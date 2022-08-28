from HistoricalData import HistoricalData
from datetime import timedelta
import yfinance as yf

class Asset:
    INTERVALS = {
        "1w": timedelta(weeks=1),
        "1d": timedelta(days=1),
        "1h": timedelta(hours=1),
        "5m": timedelta(minutes=5),
        "1m": timedelta(minutes=1)
    }

    MAX = {
        "1w": "max",
        "1d": "max",
        "1h": "730d",
        "5m": "60d",
        "1m": "7d"
    }

    def __init__(self, symbol, timeframe="1d", length=None, auto_adjust=True):
        """
        symbol: str - symbol (for example, 'SPY')
        timeframe: str - symbol for length of time of each datapoint
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.length = self.MAX[timeframe] if length is None else length
        self.auto_adjust = auto_adjust

        history = self.__get_history()

        self.open = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="Open"))
        self.close = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="Close"))
        self.high = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="High"))
        self.low = HistoricalData(dictionary=self.__get_prices_dict(history, price_type="Low"))

    def __get_history(self):
        return yf.Ticker(self.symbol).history(interval=self.timeframe, period=self.length, auto_adjust=self.auto_adjust)

    def __get_prices_dict(self, history, price_type="Close"):
        return {timestamp.to_pydatetime(): float(price) for timestamp, price in history[price_type].items()}

    def get_price_by_date(self, date):
        return self.close.get_val_by_date(date)

    def dollar_cost_average(self, period):
        """Calculates total times return of DCA"""
        return (self.close.values[-1] / self.close.values[::period]).mean()

    def lump_sum(self):
        """Calculates total times return of a lump_sum investment"""
        return self.close.values[-1] / self.close.values[0]

    def plot(self, shares=1, show=True):
        (self.close * shares).plot(label=self.symbol, show=show)
