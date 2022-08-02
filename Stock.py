from collections import OrderedDict
from datetime import datetime
import json
import matplotlib.pyplot as plt
import requests

API_KEY = "25R4JNO0E4GWP3RI"
ENDPOINT = "https://www.alphavantage.co/query"
DAILY_DATA_FUNC = "TIME_SERIES_DAILY"
OUTPUT_SIZE = "full"

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker

        params = {"function": DAILY_DATA_FUNC, "symbol": ticker, "outputsize": OUTPUT_SIZE, "apikey": API_KEY}

        response = requests.get(ENDPOINT, params).text

        self.historical = json.loads(response)["Time Series (Daily)"]

        self.prices = self._get_prices()

    def _get_prices(self):
        prices = OrderedDict()

        for date, info in self.historical.items():
            date = datetime.strptime(date, "%Y-%m-%d")
            price = float(info["4. close"])
            prices[date] = price

        return prices

    def plot(self):
        plt.plot(self.prices.keys(), self.prices.values(), label=self.ticker)
        plt.show()
