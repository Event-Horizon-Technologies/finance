from finance.Asset import Asset
from finance.HistoricalData import HistoricalData
from finance import Utils

import yfinance as yf

class Stock(Asset):
    def __init__(self, symbol, timeframe="1d", length=None, auto_adjust=True, start_date=None, end_date=None):
        self.history = self.__get_history()
        self.auto_adjust = auto_adjust
        self.length = Utils.MAX[timeframe] if length is None else length
        super().__init__(symbol, timeframe, length, auto_adjust, start_date, end_date)

    def get_ohlcv(self) -> None:
        self.open = self.__create_historical_data("Open")
        self.close = self.__create_historical_data("Close")
        self.high = self.__create_historical_data("High")
        self.low = self.__create_historical_data("Low")
        self.volume = self.__create_historical_data("Volume")
        
    @staticmethod
    def get_history(symbol, timeframe, length, auto_adjust):
        return yf.Ticker(symbol).history(interval=timeframe, period=length, auto_adjust=auto_adjust)

    def __get_history(self):
        return self.get_history(self.symbol, self.timeframe, self.length, self.auto_adjust)

    def __create_historical_data(self, price_type) -> HistoricalData:
        # the yfinance API can have bad data in the first and last row of history for some reason, thus the '[1:-1]'
        series = self.history[price_type][1:-1]
        return HistoricalData(series=series, interval=self.interval, start_date=self.start_date, end_date=self.end_date)
