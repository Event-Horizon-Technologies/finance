from finance.HistoricalData import HistoricalData
from finance import Utils

import yfinance as yf
from numpy import ndarray

class Asset:
    def __init__(self, symbol, history=None, timeframe="1d",
                 length=None, auto_adjust=True, start_date=None, end_date=None) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.length = Utils.MAX[timeframe] if length is None else length
        self.auto_adjust = auto_adjust
        self.start_date = start_date
        self.end_date = end_date
        self.history = self.__get_history() if history is None else history

        interval = Utils.INTERVALS[timeframe]

        self.open = self.__create_historical_data(interval, "Open")
        self.close = self.__create_historical_data(interval, "Close")
        self.high = self.__create_historical_data(interval, "High")
        self.low = self.__create_historical_data(interval, "Low")
        self.volume = self.__create_historical_data(interval, "Volume")

        self.start_date, self.end_date = self.close.start_date, self.close.end_date

    @staticmethod
    def get_history(symbol, timeframe, length, auto_adjust):
        return yf.Ticker(symbol).history(interval=timeframe, period=length, auto_adjust=auto_adjust)

    def __get_history(self):
        return Asset.get_history(self.symbol, self.timeframe, self.length, self.auto_adjust)

    def __create_historical_data(self, interval="1d", price_type="Close") -> HistoricalData:
        # the yfinance API can have bad data in the first and last row of history for some reason, thus the '[1:-1]'
        series = self.history[price_type][1:-1]
        return HistoricalData(series=series, interval=interval, start_date=self.start_date, end_date=self.end_date)

    def get_price_by_date(self, date) -> float:
        return self.close.get_val_by_date(date)

    def dollar_cost_average(self, period) -> float:
        return (self.close.values[-1] / self.close.values[::period]).mean()

    def lump_sum(self) -> float:
        return self.close.values[-1] / self.close.values[0]

    def plot(self, shares=1, show=True) -> None:
        (self.close * shares).plot(label=self.symbol, show=show)
