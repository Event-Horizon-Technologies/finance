import numpy as np
from sortedcontainers import SortedDict
from Asset import Asset


class Investment:
    def __init__(self, symbol, timeframe="1d", length="max"):
        self.asset = Asset(symbol, timeframe, length)
        self.transactions = SortedDict()
        self.shares = 0.0
        self.average_cost = 0.0
        self.diversity = 0.0

    @property
    def start_date(self):
        return self.asset.prices.start_date

    @property
    def end_date(self):
        return self.asset.prices.end_date

    @property
    def interval(self):
        return self.asset.prices.interval

    @property
    def prices(self):
        return self.asset.prices.array

    @property
    def equity(self):
        return self.shares * self.prices[-1]

    def update_diversification(self, total_equity):
        self.diversity = self.equity / total_equity

    def buy(self, date, amount):
        self.transactions[date] = amount
        self.shares += amount / self.prices.get_val_by_date(date)

    def sell(self, date, amount):
        if amount > self.equity:
            return False

        self.transactions[date] = -amount
        self.shares -= amount / self.prices.get_val_by_date(date)

        return True

    def get_history(self):
        history = np.copy(self.prices)
        shares = srt_idx = 0
        cash = sum(self.transactions.values())

        for date, amount in self.transactions.items():
            curr_idx = (date - self.start_date) / self.interval

            history[srt_idx:curr_idx] = cash + history[srt_idx:curr_idx] * shares

            cash -= amount
            shares += amount / self.prices[curr_idx]
            srt_idx = curr_idx

        history[srt_idx:] = cash + history[srt_idx:] * shares

        return history
