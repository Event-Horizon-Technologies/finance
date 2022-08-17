import numpy as np
from sortedcontainers import SortedDict
from Asset import Asset
import matplotlib.pyplot as plt


class Investment:
    def __init__(self, symbol, timeframe):
        self.asset = Asset(symbol, timeframe)
        self.quantity = 0.0

    def buy(self, amount):
        self.quantity += amount

    def sell(self, amount):
        self.quantity -= amount

    def get_equity(self, date):
        return self.quantity * self.asset.get_price_by_date(date)
