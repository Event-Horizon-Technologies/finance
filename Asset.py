from sortedcontainers import SortedDict
from HistoricalData import HistoricalData
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

class Asset:
    def __init__(self, ticker, timeframe="1d", length="max"):
        """
        ticker: str - symbol (for example, 'SPY')
        timeframe: str - symbol for length of time of each datapoint
        """
        self.ticker = ticker
        self.timeframe = timeframe
        self.length = length
        self.indicators = {}
        self.prices = HistoricalData(dictionary=self.__get_prices_dict())

    def __get_prices_dict(self, price_type="Close"):
        historical = yf.Ticker(self.ticker).history(interval=self.timeframe, period=self.length)
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

    #TODO: code and optimize
    def get_EMA_prices(self, period=200):
        """Returns values of Exponential Moving Average for a specific period"""
        k = 2.0 / (period + 1)

        ema = SortedDict()

        dates = list(self.prices.keys())
        prices = list(self.prices.values())

        size = len(dates)

        sum = 0.0
        for i in range(size):
            if i < period:
                sum += prices[i]

                if i == period - 1:
                    ema[dates[i]] = sum / period
            else:
                ema[dates[i]] = k * prices[i] + (1.0 - k) * ema[dates[i-1]]

        self.indicators["ema"] = ema

        return ema

    def dollar_cost_average(self, period):
        """Calculates total times return of DCA"""
        i = harmonic_sum = n = 0

        for price in self.prices.values():
            if i % period == 0:
                harmonic_sum += 1 / price
                n += 1
            i += 1

        harmonic_mean = n / harmonic_sum
        final_price = list(self.prices.values())[-1]
        return final_price / harmonic_mean

    def lump_sum(self):
        """Calculates total times return of a lump_sum investment"""
        beginning_price = list(self.prices.values())[0]
        final_price = list(self.prices.values())[-1]
        return final_price / beginning_price

    def plot(self):
        self.prices.plot(self.ticker)
        for label, data in self.indicators.items():
            data.plot(label)
        plt.legend(loc='best', prop={'size': 20})
        plt.show()
