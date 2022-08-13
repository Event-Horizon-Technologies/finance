from Investment import Investment
from warnings import warn

class Portfolio:
    def __init__(self):
        self.investments= {}
        self.timeframe = None
        self.length = None
        self.total_equity = None

    def buy_asset(self, ticker, amount):
        if ticker not in self.investments:
            self.investments[ticker] = Investment(ticker, self.timeframe, self.length)

        self.investments[ticker].buy(amount)

    def sell_asset(self, ticker, amount):
        if ticker in self.investments:
            self.investments[ticker].sell(amount)
        else:
            warn(f"Attempted to sell {ticker} without owning any, ignored")


    def __update_diversifications(self):
        # should this function set self.total_equity or let this be done elsewhere ?
        self.total_equity = self.__calc_total_equity()

        for investment in self.investments.values():
            investment.update_diversification(self.total_equity)

    def __calc_total_equity(self):
        return sum([investment.get_equity() for investment in self.investments.values()])

    def set_timeframe(self, timeframe):
        self.timeframe = timeframe

