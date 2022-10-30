import math
from abc import ABC, abstractmethod

import numba as nb
import numpy as np

from finance.HistoricalData import HistoricalData


class Indicator(ABC):
    def __init__(self, label=None, scatter=False) -> None:
        self.label = self.__class__.__name__ if label is None else label
        self.scatter = scatter

    @abstractmethod
    def get_values(self, asset=None) -> np.ndarray:
        pass

    def create_indicator(self, asset=None):
        return HistoricalData(
            values=self.get_values(asset),
            interval=asset.close.interval,
            end_date=asset.close.end_date,
            label=self.label,
            scatter=self.scatter,
        )

    def create_neural_net_data(self, asset=None, prediction_offset=30) -> np.ndarray:
        # The neural network will be trained to predict the price 'prediction_offset' timesteps in the future
        # Means we have to trim the end of array so the prediction won't go out of bounds
        return np.log(self.get_values(asset) / asset.close.values)[:-prediction_offset]


class SMA(Indicator):
    def __init__(self, label=None, period=200) -> None:
        super().__init__(label)
        self.period = period

    def get_values(self, asset=None) -> np.ndarray:
        cum_sum = asset.close.values.cumsum()
        return (
            np.append(
                cum_sum[self.period - 1],
                cum_sum[self.period :] - cum_sum[: -self.period],
            )
            / self.period
        )


class EMA(Indicator):
    def __init__(self, label=None, period=200) -> None:
        super().__init__(label)
        self.period = period

    def get_values(self, asset=None) -> np.ndarray:
        k = 2.0 / (self.period + 1)
        return (
            np.frompyfunc(lambda x, y: (1 - k) * x + k * y, 2, 1)
            .accumulate(asset.close.values)
            .astype(np.float)
        )


class PSAR(Indicator):
    def __init__(self, label=None, increment=0.02, max_alpha=0.2) -> None:
        super().__init__(label)
        self.increment = increment
        self.max_alpha = max_alpha

    def get_values(self, asset=None) -> np.ndarray:
        return self.psar(
            asset.close.values,
            asset.high.values,
            asset.low.values,
            self.increment,
            self.max_alpha,
        )

    @staticmethod
    @nb.njit(cache=True)
    def psar(close_arr, high_arr, low_arr, increment, max_alpha) -> np.ndarray:
        uptrend = close_arr[0] < close_arr[1]
        values = np.empty(len(low_arr))
        values[0] = sar = low_arr[0] if uptrend else high_arr[0]
        ep = -math.inf if uptrend else math.inf
        alpha = 0.0

        for i in range(1, len(low_arr)):
            low, high = low_arr[i], high_arr[i]

            # if we reach a new ep
            if (uptrend and high > ep) or (not uptrend and low < ep):
                ep = high if uptrend else low
                alpha = min(max_alpha, alpha + increment)

            sar = alpha * ep + (1.0 - alpha) * sar

            # if trend switch
            if (uptrend and sar >= low) or (not uptrend and sar <= high):
                uptrend = not uptrend
                sar = ep
                ep = -math.inf if uptrend else math.inf
                alpha = 0.0

            values[i] = sar

        return values


class OBV(Indicator):
    def __init__(self, label=None) -> None:
        super().__init__(label)

    def get_values(self, asset=None) -> np.ndarray:
        volume, open, close = asset.volume.values, asset.open.values, asset.close.values
        volume[close < open] *= -1
        return volume.cumsum()
