from finance.HistoricalData import HistoricalData

import math
import numba as nb
import numpy as np

@nb.experimental.jitclass([("label", nb.types.unicode_type), ("period", nb.int64)])
class SMA:
    def __init__(self, label="SMA", period=200):
        self.label = label
        self.period = period

    def create_indicator(self, asset):
        cumsum = asset.close.values.cumsum()
        values = np.append(cumsum[self.period - 1], cumsum[self.period:] - cumsum[:-self.period]) / self.period
        start_date = asset.start_date + (self.period - 1) * asset.interval
        return HistoricalData(values, asset.interval, start_date, asset.end_date, self.label, False)

@nb.experimental.jitclass([("label", nb.types.unicode_type), ("period", nb.int64)])
class EMA:
    def __init__(self, label="EMA", period=200):
        self.label = label
        self.period = period

    def create_indicator(self, asset):
        k = 2.0 / (self.period + 1); n = len(asset.close.values)
        values = asset.close.values.copy()
        for i in range(1, n):
            values[i] = (1.0 - k) * values[i-1] + k * values[i]
        return HistoricalData(values, asset.interval, asset.start_date, asset.end_date, self.label, False)

@nb.experimental.jitclass([("label", nb.types.unicode_type), ("increment", nb.float64), ("max_alpha", nb.float64)])
class PSAR:
    def __init__(self, label="PSAR", increment=0.02, max_alpha=0.2):
        self.label = label
        self.increment = increment
        self.max_alpha = max_alpha

    def create_indicator(self, asset):
        values = self.psar(asset.close.values, asset.high.values, asset.low.values)
        return HistoricalData(values, asset.interval, asset.start_date, asset.end_date, self.label, True)

    def psar(self, close_arr, high_arr, low_arr):
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
                alpha = min(self.max_alpha, alpha + self.increment)

            sar = alpha * ep + (1.0 - alpha) * sar

            # if trend switch
            if (uptrend and sar >= low) or (not uptrend and sar <= high):
                uptrend = not uptrend
                sar = ep
                ep = -math.inf if uptrend else math.inf
                alpha = 0.0

            values[i] = sar

        return values
