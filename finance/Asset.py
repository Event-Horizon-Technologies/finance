import numpy as np

from finance.AlphaVantage import AlphaVantage
from finance.HistoricalData import HistoricalData
from finance import Utils

from abc import ABC, abstractmethod

class Asset(ABC):
    def __init__(self, symbol, timeframe="1day", start_date=None, end_date=None):
        self.symbol = symbol
        self.timeframe = timeframe
        self.start_date = start_date
        self.end_date = end_date
        self.interval = Utils.INTERVALS[timeframe]
        self.open = self.close = self.high = self.low = self.volume = self.market_cap = None

        self.get_history()

    @abstractmethod
    def get_history(self): pass


    def get_price_by_date(self, date):
        return self.close.get_val_by_date(date)

    def dollar_cost_average(self, period):
        return (self.close.values[-1] / self.close.values[::period]).mean()

    def lump_sum(self):
        return self.close.values[-1] / self.close.values[0]

    def plot(self, shares=1, show=True):
        (self.close * shares).plot(label=self.symbol, show=show)
