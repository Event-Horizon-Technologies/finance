import Utils
from HistoricalData import HistoricalData

import numpy as np
import yfinance as yf

class Asset:
    INTERVALS = {
        "1d": np.timedelta64(1, 'D'),
        "1h": np.timedelta64(1, 'h'),
        "5m": np.timedelta64(5, 'm'),
        "1m": np.timedelta64(1, 'm')
    }

    MAX = {
        "1d": "max",
        "1h": "730d",
        "5m": "60d",
        "1m": "7d"
    }

    def __init__(self, symbol, timeframe="1d", length=None, auto_adjust=True):
        self.symbol = symbol
        self.timeframe = timeframe
        self.length = self.MAX[timeframe] if length is None else length
        self.auto_adjust = auto_adjust

        history = self.__get_history()
        interval = self.INTERVALS[timeframe]

        self.open = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="Open"), interval=interval)
        self.close = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="Close"), interval=interval)
        self.high = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="High"), interval=interval)
        self.low = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="Low"), interval=interval)

    def __get_history(self):
        return yf.Ticker(self.symbol).history(interval=self.timeframe, period=self.length, auto_adjust=self.auto_adjust)

    @staticmethod
    def __get_prices_dict(history, price_type="Close"):
        # the yfinance API can have bad data in the last row of history for some reason, thus the '[:-1]'
        return {Utils.create_np_datetime(timestamp): float(price) for timestamp, price in history[price_type][:-1].items()}

    def get_price_by_date(self, date):
        return self.close.get_val_by_date(date)

    def dollar_cost_average(self, period):
        return (self.close.values[-1] / self.close.values[::period]).mean()

    def lump_sum(self):
        return self.close.values[-1] / self.close.values[0]

    def plot(self, shares=1, show=True):
        (self.close * shares).plot(label=self.symbol, show=show)