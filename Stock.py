from sortedcontainers import SortedDict
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os.path
import requests

API_KEY = "25R4JNO0E4GWP3RI"
ENDPOINT = "https://www.alphavantage.co/query"
DAILY_DATA_FUNC = "TIME_SERIES_DAILY"
OUTPUT_SIZE = "full"

class Stock:
    def __init__(self, ticker, update=False):
        self.ticker = ticker
        self.file = ticker + ".json"
        self.indicators = {}

        if update or not os.path.exists(ticker + ".json"):
            self.update()
        else:
            self.read()

    def __get_prices(self):
        prices = SortedDict()

        for date, info in self.historical.items():
            date = datetime.strptime(date, "%Y-%m-%d")
            price = float(info["4. close"])
            prices[date] = price

        return prices

    def __get_attrs_from_json(self, response):
        self.historical = json.loads(response)["Time Series (Daily)"]
        self.prices = self.__get_prices()

    def read(self):
        with open(self.file) as f:
            response = f.read()
            self.__get_attrs_from_json(response)

    def update(self):
        params = {"function": DAILY_DATA_FUNC, "symbol": self.ticker, "outputsize": OUTPUT_SIZE, "apikey": API_KEY}
        response = requests.get(ENDPOINT, params).text
        self.__get_attrs_from_json(response)

        with open(self.file, "w") as f:
            f.write(response)

     # TODO: optimize with numpy?
    def get_SMA_prices(self, period=200):
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
    def _get_EMA_prices(self, period, k):
        pass

    def plot(self):
        plt.plot(self.prices.keys(), self.prices.values(), label=self.ticker)

        for label, data in self.indicators.items():
            plt.plot(data.keys(), data.values(), label=label)

        plt.show()
