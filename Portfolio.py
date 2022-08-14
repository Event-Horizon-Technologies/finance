from Investment import Investment
from warnings import warn

class Portfolio:
    def __init__(self):
        self.investments = {}
        self.timeframe = None
        self.length = None
        self.total_equity = 0.0

    def buy_asset(self, symbol, date, amount):
        if symbol not in self.investments:
            self.investments[symbol] = Investment(symbol, self.timeframe, self.length)

        self.investments[symbol].buy(date, amount)
        self.__update_attributes()

    def sell_asset(self, symbol, amount):
        if symbol in self.investments:
            if not self.investments[symbol].sell(amount):
                warn(f"Attempted to sell more {symbol} than you own, ignored")

            if self.investments[symbol].get_equity() <= 0:
                del self.investments[symbol]
            
            self.__update_attributes()
        else:
            warn(f"Attempted to sell {symbol} without owning any, ignored")
        
    def __update_attributes(self):
        self.__update_total_equity()
        self.__update_diversifications()

    def __update_diversifications(self):
        for investment in self.investments.values():
            investment.update_diversification(self.total_equity)

    def __update_total_equity(self):
        self.total_equity = sum([investment.equity for investment in self.investments.values()])
