from Asset import Asset
from Investment import Investment
from warnings import warn
from Utils import *

class Simulator:
    def __init__(self, start_date, end_date, timeframe="1d", cash=1.0):
        self.now = start_date
        self.investments = {}
        self.indicator_data = {}
        self.strat_hist = {}
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

    def plot(self, plot_assets=False, plot_indicators=False):
        plt.plot(self.strat_hist.keys(), self.strat_hist.values(), label="Strategy")

        if plot_assets or plot_indicators:
            for symbol, investment in self.investments.items():
                asset = investment.asset
                shares = self.initial_cash / asset.get_price_by_date(self.start_date)

                if plot_assets:
                    asset.plot(shares=shares, show=False)

                if plot_indicators:
                    for label, data in self.indicator_data[symbol].items():
                        (data * shares).plot(show=False, label=f"{symbol} {label}")

        show_plot()

    def get_return(self):
        return (self.get_equity() + self.cash) / self.initial_cash

    def get_alpha(self):
        if len(self.investments) > 1:
            raise Exception("Alpha only makes sense with one asset")

        return self.get_return() / list(self.investments.values())[0].asset.lump_sum()

    def run(self, strategy):
        # create symbols and indicators
        for symbol in strategy.symbols:
            self.__create_investment(symbol)
            self.indicator_data[symbol] = {}
            for indicator in strategy.indicators:
                historical_data = indicator.create_indicator(self.investments[symbol].asset)
                self.indicator_data[symbol][historical_data.label] = historical_data

        # run strategy
        while self.now <= self.end_date:
            self.make_transactions(strategy.strategy(self))
            self.strat_hist[self.now] = self.get_equity() + self.cash
            self.now += self.interval
