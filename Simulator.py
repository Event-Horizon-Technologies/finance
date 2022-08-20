from Asset import Asset
from Investment import Investment
from warnings import warn
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, start_date, end_date, timeframe="1d", cash=1.0):
        self.now = start_date
        self.investments = {}
        self.indicators = {}
        self.interval = Asset.INTERVALS[timeframe]
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.cash = cash
        self.initial_cash = cash

    def __create_investment(self, symbol):
        self.investments[symbol] = Investment(symbol, self.timeframe)

    def buy(self, symbol, amount):
        if amount > self.cash:
            warn(f"Attempted to buy {amount} of {symbol} with only {self.cash} cash")
            return False
            
        if symbol not in self.investments:
            self.__create_investment(symbol)

        self.investments[symbol].buy(self.now, amount)
        self.cash -= amount
        
        return True

    def sell(self, symbol, amount):
        if symbol not in self.investments:
            warn(f"Attempted to sell asset {symbol} which does not exist")
            return False
            
        equity = self.investments[symbol].get_equity(self.now)
        if amount > equity:
            warn(f"Attempted to sell {amount} of {symbol} with only {equity} equity")
            return False

        self.investments[symbol].sell(self.now, amount)
        self.cash += amount

        return True

    def get_equity(self):
        return sum(investment.get_equity(self.now) for investment in self.investments.values())

    def make_transactions(self, transactions):
        for symbol, amount in transactions.items():
            if amount > 0:
                self.buy(symbol, amount)
            else:
                self.sell(symbol, -amount)

    def run(self, strategy):
        for symbol in strategy.symbols:
            self.__create_investment(symbol)
            self.indicators[symbol] = {}
            for indicator in strategy.indicators:
                historical_data = indicator(self.investments[symbol].asset)
                self.indicators[symbol][historical_data.label] = historical_data

        strat_hist = {}
        while self.now <= self.end_date:
            self.make_transactions(strategy.strategy(self))
            strat_hist[self.now] = self.get_equity() + self.cash
            self.now += self.interval

        self.indicators[strategy.symbols[0]]["EMA"].plot()
        plt.plot(strat_hist.keys(), strat_hist.values(), label="Strategy")

        return (self.get_equity() + self.cash) / self.initial_cash
