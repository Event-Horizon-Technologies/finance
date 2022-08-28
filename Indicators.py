from abc import ABC, abstractmethod
from HistoricalData import HistoricalData
import numpy as np
import math


class Indicator(ABC):
    def __init__(self, label=None):
        self.label = self.__class__.__name__ if label is None else label

    def create_price_indicator(self, asset, values, scatter=False):
        return HistoricalData(values=values, interval=asset.close.interval, end_date=asset.close.end_date,
                              label=self.label, scatter=scatter)

    @abstractmethod
    def create_indicator(self, asset=None):
        pass

class SMA(Indicator):
    def __init__(self, label=None, period=200):
        super().__init__(label)
        self.period = period

    def create_indicator(self, asset=None):
        """Returns values of Simple Moving Average for a specific period"""
        cumsum = asset.close.values.cumsum()
        values = np.append(cumsum[self.period - 1], cumsum[self.period:] - cumsum[:-self.period]) / self.period
        return self.create_price_indicator(asset, values)

class EMA(Indicator):
    def __init__(self, label=None, period=200):
        super().__init__(label)
        self.period = period

    def create_indicator(self, asset=None):
        """Returns values of Exponential Moving Average for a specific period"""
        k = 2.0 / (self.period + 1)
        values = np.frompyfunc(lambda x, y: (1-k)*x + k*y, 2, 1).accumulate(asset.close.values)
        return self.create_price_indicator(asset, values)

class PSAR(Indicator):
    def __init__(self, label=None, increment=0.02, max_alpha=0.2):
        super().__init__(label)
        self.increment = increment
        self.max_alpha = max_alpha

    def create_indicator(self, asset=None):
        uptrend = asset.close.values[0] < asset.close.values[1]
        sar = asset.low.values[0] if uptrend else asset.high.values[0]
        ep = -math.inf if uptrend else math.inf
        alpha = 0
        values = []

        for high, low in zip(asset.high.values[1:], asset.low.values[1:]):
            # if we reach a new ep
            if (uptrend and high > ep) or (not uptrend and low < ep):
                ep = high if uptrend else low
                alpha = min(self.max_alpha, alpha + self.increment)

            sar = alpha * ep + (1.0 - alpha) * sar

            # if trend switch
            if (uptrend and sar >= low) or (not uptrend and sar <= high):
                uptrend = not uptrend
                sar = ep
                ep = -math.inf if uptrend else math.inf
                alpha = 0

            values.append(sar)

        return self.create_price_indicator(asset, np.array(values), scatter=True)
