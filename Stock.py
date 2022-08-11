from sortedcontainers import SortedDict
from HistoricalData import HistoricalData
import matplotlib.pyplot as plt
import yfinance as yf

class Stock:
    def __init__(self, ticker, timeframe="1d", length="max"):
        """
        ticker: str - symbol (for example, 'SPY')
        timeframe: str - symbol for length of time of each datapoint
        """
        self.ticker = ticker
        self.indicators = {}

        self.historical = yf.Ticker(ticker).history(interval=timeframe, period=length)
        self.prices = self.__get_prices()

        prices = HistoricalData(self.prices)

        self.prices = prices.to_dict()

    def __get_prices(self, price_type="Close"):
        return {timestamp.to_pydatetime(): float(price) for timestamp, price in self.historical[price_type].items()}

     # TODO: optimize with numpy?
    def get_SMA_prices(self, period=200):
        """Returns values of Simple Moving Average for a specific period"""
        sma = SortedDict()

        dates = list(self.prices.keys())
        prices = list(self.prices.values())

        size = len(dates)

        j = 0
        sum = 0.0
        for i in range(size):
            if i < period:
                sum += prices[i]

                if i == period - 1:
                    sma[dates[i]] = sum / period
            else:
                sum += prices[i] - prices[j]

                sma[dates[i]] = sum / period

                j += 1

        self.indicators["sma"] = sma

        return sma
        
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
        plt.plot(self.prices.keys(), self.prices.values(), label=self.ticker)

        for label, data in self.indicators.items():
            plt.plot(data.keys(), data.values(), label=label)

        plt.legend(loc='best', prop={'size': 20})

        plt.show()
