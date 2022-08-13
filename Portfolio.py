from Investment import Investment
from warnings import warn

class Portfolio:
    def __init__(self):
        self.investments= {}
        self.timeframe = None
        self.length = None
        self.total_equity = None

    def buy_asset(self, symbol, amount):
        if symbol not in self.investments:
            self.investments[symbol] = Investment(symbol, self.timeframe, self.length)

        self.investments[symbol].buy(amount)

    def sell_asset(self, symbol, amount):
        if symbol in self.investments:
            self.investments[symbol].sell(amount)
        else:
            warn(f"Attempted to sell {symbol} without owning any, ignored")


    def __update_diversifications(self):
        # should this function set self.total_equity or let this be done elsewhere ?
        self.total_equity = self.__calc_total_equity()

        for investment in self.investments.values():
            investment.update_diversification(self.total_equity)

    def __calc_total_equity(self):
        return sum([investment.get_equity() for investment in self.investments.values()])

    def set_timeframe(self, timeframe):
        self.timeframe = timeframe

