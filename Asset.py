from HistoricalData import HistoricalData
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

class Asset:
    def __init__(self, symbol, timeframe="1d", length="max"):
        """
        symbol: str - symbol (for example, 'SPY')
        timeframe: str - symbol for length of time of each datapoint
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.length = length
        self.indicators = {}
        self.prices = HistoricalData(dictionary=self.__get_prices_dict())

    def __get_prices_dict(self, price_type="Close"):
        historical = yf.ticker(self.symbol).history(interval=self.timeframe, period=self.length)
        return {timestamp.to_pydatetime(): float(price) for timestamp, price in historical[price_type].items()}

    def get_SMA_prices(self, period=200):
        """Returns values of Simple Moving Average for a specific period"""
        cumsum = self.prices.array.cumsum()
        self.indicators["SMA"] = HistoricalData(
            array=np.append(cumsum[period-1], cumsum[period:] - cumsum[:-period]) / period,
            interval=self.prices.interval,
            end_date=self.prices.end_date
        )
        return self.indicators["SMA"]

    def get_EMA_prices(self, period=200):
        """Returns values of Exponential Moving Average for a specific period"""
        k = 2.0 / (period + 1)
        self.indicators["EMA"] = HistoricalData(
            array=np.frompyfunc(lambda x, y: (1-k)*x + k*y, 2, 1).accumulate(self.prices.array),
            interval=self.prices.interval,
            end_date=self.prices.end_date
        )
        return self.indicators["EMA"]

    def dollar_cost_average(self, period):
        """Calculates total times return of DCA"""
        return (self.prices.array[-1] / self.prices.array[::period]).mean()

    def lump_sum(self):
        """Calculates total times return of a lump_sum investment"""
        return self.prices.array[-1] / self.prices.array[0]

    def plot(self):
        self.prices.plot(self.symbol)
        for label, data in self.indicators.items():
            data.plot(label)
        plt.legend(loc='best', prop={'size': 20})
        plt.show()
