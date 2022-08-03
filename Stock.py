from genericpath import isdir
from sortedcontainers import SortedDict
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os
import requests

API_KEY = "25R4JNO0E4GWP3RI"
ENDPOINT = "https://www.alphavantage.co/query"
DAILY_DATA_FUNC = "TIME_SERIES_DAILY"
OUTPUT_SIZE = "full"
JSON_DIR = "json"

class Stock:
    def __init__(self, ticker, update=False):
        """Constructor for Stock class"""

        self.ticker = ticker
        self.file = JSON_DIR + "/" + ticker + ".json"
        self.indicators = {}

        if not os.path.isdir(JSON_DIR):
            os.mkdir(JSON_DIR)

        if update or not os.path.exists(self.file):
            self.update()
        self.read()

    def __get_prices(self):
        """Gets the prices from data"""
        prices = SortedDict()

        for date, info in self.historical.items():
            date = datetime.strptime(date, "%Y-%m-%d")
            price = float(info["4. close"])
            prices[date] = price

        return prices

    def __get_attrs_from_json(self, response):
        """Reads data from json and updates data in this Stock object"""

        self.historical = json.loads(response)["Time Series (Daily)"]
        self.prices = self.__get_prices()

    def read(self):
        """Reads data from local database (currently json) and updates this Stock object"""
        
        with open(self.file) as f:
            response = f.read()
            self.__get_attrs_from_json(response)

    def update(self):
        """Pulls data from source and updates the local database (currently json)"""

        params = {"function": DAILY_DATA_FUNC, "symbol": self.ticker, "outputsize": OUTPUT_SIZE, "apikey": API_KEY}
        response = requests.get(ENDPOINT, params).text

        with open(self.file, "w") as f:
            f.write(response)

     # TODO: optimize with numpy?
    def get_SMA_prices(self, period=200):
        """Computes and returns data for a simple moving average for a specific period"""

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
        """Computes and returns data for an exponential moving average with a specific period"""

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

    def plot(self):
        """Handles plotting data from Stock class"""
        plt.plot(self.prices.keys(), self.prices.values(), label=self.ticker)

        for label, data in self.indicators.items():
            plt.plot(data.keys(), data.values(), label=label)

        plt.legend(loc='best', prop={'size': 20})

        plt.show()
