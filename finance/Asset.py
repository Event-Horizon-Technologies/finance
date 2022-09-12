from finance.HistoricalData import HistoricalData

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

    def __init__(self, symbol, history=None, timeframe="1d",
                 length=None, auto_adjust=True, start_date=None, end_date=None):
        self.symbol = symbol
        self.timeframe = timeframe
        self.length = self.MAX[timeframe] if length is None else length
        self.auto_adjust = auto_adjust
        self.start_date = start_date
        self.end_date = end_date
        self.history = self.__get_history() if history is None else history

        interval = self.INTERVALS[timeframe]

        self.open = self.__create_historical_data(interval, "Open")
        self.close = self.__create_historical_data(interval, "Close")
        self.high = self.__create_historical_data(interval, "High")
        self.low = self.__create_historical_data(interval, "Low")

        self.start_date, self.end_date = self.close.start_date, self.close.end_date

    @staticmethod
    def get_history(symbol, timeframe, length, auto_adjust):
        return yf.Ticker(symbol).history(interval=timeframe, period=length, auto_adjust=auto_adjust)

    def __get_history(self):
        return Asset.get_history(self.symbol, self.timeframe, self.length, self.auto_adjust)

    def __create_historical_data(self, interval="1d", price_type="Close"):
        # the yfinance API can have bad data in the last row of history for some reason, thus the '[:-1]'
        series = self.history[price_type][:-1]
        return HistoricalData(series=series, interval=interval, start_date=self.start_date, end_date=self.end_date)

    def get_price_by_date(self, date):
        return self.close.get_val_by_date(date)

    def dollar_cost_average(self, period):
        return (self.close.values[-1] / self.close.values[::period]).mean()

    def lump_sum(self):
        return self.close.values[-1] / self.close.values[0]

    def plot(self, shares=1, show=True):
        (self.close * shares).plot(label=self.symbol, show=show)
