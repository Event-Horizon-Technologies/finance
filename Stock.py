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
        self.ticker = ticker
        self.file = JSON_DIR + "/" + ticker + ".json"
        self.indicators = {}

        if not os.path.isdir(JSON_DIR):
            os.mkdir(JSON_DIR)

        if update or not os.path.exists(self.file):
            json_ = self.get_json_from_api()
            self.write_json_to_file(json_)
        else:
            json_ = self.read_json_from_files()

        self.__get_attrs_from_json(json_)




    def __get_prices(self):
        prices = SortedDict()

        for date, info in self.historical.items():
            date = datetime.strptime(date, "%Y-%m-%d")
            price = float(info["4. close"])
            prices[date] = price

        return prices

    def __get_attrs_from_json(self, json_):
        self.historical = json.loads(json_)["Time Series (Daily)"]
        self.prices = self.__get_prices()

    def read_json_from_files(self):
        with open(self.file) as f:
            return f.read()

    def write_json_to_file(self, json_):
        with open(self.file, "w") as f:
            f.write(json_)

    def get_json_from_api(self):
        params = {"function": DAILY_DATA_FUNC, "symbol": self.ticker, "outputsize": OUTPUT_SIZE, "apikey": API_KEY}
        return requests.get(ENDPOINT, params).text

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
    def get_EMA_prices(self, period=200):
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


    def dollar_cost_average(self, amount, period, start_date, end_date):
        """Calculates DCA"""
        num_of_times_invested = "not sure how to do this"
        final_price = self.prices[end_date]
        harmonic_mean = self.__get_harmonic_mean(period, start_date, end_date)
        return_rate = (final_price / harmonic_mean) - 1

        return amount * num_of_times_invested * return_rate

    def __get_harmonic_mean(self, period, start_date, end_date):
        """Calculate harmonic mean"""

    def lump_sum(self, amount, start_date, end_date):
        """Calculates lump_sum investment results"""
        return_rate = self.prices[end_date] / self.prices[start_date]
        return amount * return_rate



    def plot(self):
        plt.plot(self.prices.keys(), self.prices.values(), label=self.ticker)

        for label, data in self.indicators.items():
            plt.plot(data.keys(), data.values(), label=label)

        plt.legend(loc='best', prop={'size': 20})

        plt.show()
