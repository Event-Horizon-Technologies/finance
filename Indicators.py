from abc import ABC, abstractmethod
from HistoricalData import HistoricalData
import numpy as np


class Indicator(ABC):
    def __init__(self):
        self.label = self.__class__.__name__

    def create_price_indicator(self, asset, values):
        return HistoricalData(values=values, interval=asset.prices.interval, end_date=asset.prices.end_date, label=self.label)

    @abstractmethod
    def create_indicator(self, asset=None):
        return None

class SMA(Indicator):
    def __init__(self, period=200):
        super(SMA, self).__init__()
        self.period = period

    def create_indicator(self, asset=None):
        """Returns values of Simple Moving Average for a specific period"""
        cumsum = asset.prices.values.cumsum()
        values = np.append(cumsum[self.period - 1], cumsum[self.period:] - cumsum[:-self.period]) / self.period
        return self.create_price_indicator(asset, values)

class EMA(Indicator):
    def __init__(self, period=200):
        super(EMA, self).__init__()
        self.period = period

    def create_indicator(self, asset=None):
        """Returns values of Exponential Moving Average for a specific period"""
        k = 2.0 / (self.period + 1)
        values = np.frompyfunc(lambda x, y: (1-k)*x + k*y, 2, 1).accumulate(asset.prices.values)
        return self.create_price_indicator(asset, values)
