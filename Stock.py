from sortedcontainers import SortedDict
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os
import requests

API_KEY = "25R4JNO0E4GWP3RI"
ENDPOINT = "https://www.alphavantage.co/query"
OUTPUT_SIZE = "full"
DATATYPE = "json"
JSON_DIR = "json"

FUNC_STR = "func"
INTERVAL_STR = "interval"
DATE_FORMAT = "date_format"

API_ARGS = {
    "1m": {FUNC_STR: "TIME_SERIES_INTRADAY", INTERVAL_STR: "1min", DATE_FORMAT: "%Y-%m-%d %X"},
    "5m": {FUNC_STR: "TIME_SERIES_INTRADAY", INTERVAL_STR: "5min", DATE_FORMAT: "%Y-%m-%d %X"},
    "15m": {FUNC_STR: "TIME_SERIES_INTRADAY", INTERVAL_STR: "15min", DATE_FORMAT: "%Y-%m-%d %X"},
    "30m": {FUNC_STR: "TIME_SERIES_INTRADAY", INTERVAL_STR: "30min", DATE_FORMAT: "%Y-%m-%d %X"},
    "1h": {FUNC_STR: "TIME_SERIES_INTRADAY", INTERVAL_STR: "60min", DATE_FORMAT: "%Y-%m-%d %X"},
    "D": {FUNC_STR: "TIME_SERIES_DAILY", INTERVAL_STR: None, DATE_FORMAT: "%Y-%m-%d"},
    "W": {FUNC_STR: "TIME_SERIES_WEEKLY", INTERVAL_STR: None, DATE_FORMAT: "%Y-%m-%d"},
    "M": {FUNC_STR: "TIME_SERIES_MONTHLY", INTERVAL_STR: None, DATE_FORMAT: "%Y-%m-%d"}
}

class Stock:
    def __init__(self, ticker, timeframe="D", update=False):
        if timeframe not in API_ARGS:
            raise Exception(f"{timeframe} is not a valid timeframe!")

        self.ticker = ticker
        self.file = JSON_DIR + "/" + ticker + "-" + timeframe + ".json"
        self.indicators = {}
        self.api_func = API_ARGS[timeframe][FUNC_STR]
        self.api_interval = API_ARGS[timeframe][INTERVAL_STR]
        self.date_format = API_ARGS[timeframe][DATE_FORMAT]
        self.timeframe = timeframe

        if not os.path.isdir(JSON_DIR):
            os.mkdir(JSON_DIR)

        if update or not os.path.exists(self.file):
            json_ = self.get_json_from_api()
            self.write_json_to_file(json_)
        else:
            json_ = self.read_json_from_files()

        self.__load_attrs_from_json(json_)

    def __get_prices(self):
        prices = SortedDict()

        for date, info in self.historical.items():
            date = datetime.strptime(date, self.date_format)
            price = float(info["4. close"])
            prices[date] = price

        return prices

    def __load_attrs_from_json(self, json_):
        data = json.loads(json_)
        # get key for historical data
        # there is only one other key besides 'Meta Data'
        key = [key for key in data.keys() if key != "Meta Data"][0]
        self.historical = data[key]
        self.prices = self.__get_prices()

    def read_json_from_files(self):
        with open(self.file) as f:
            return f.read()

    def write_json_to_file(self, json_):
        with open(self.file, "w") as f:
            f.write(json_)

    def get_json_from_api(self):
        params = {
            "function": self.api_func,
            "symbol": self.ticker,
            "interval": self.api_interval,
            "outputsize": OUTPUT_SIZE,
            "apikey": API_KEY,
            "datatype": DATATYPE
        }
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
