from xmlrpc.client import Boolean
from finance.Asset import Asset
from finance.Investment import Investment
from finance import Utils

import matplotlib.pyplot as plt
from warnings import warn

class Simulator:
    def __init__(self, strategy, start_date, end_date, timeframe="1d", cash=1.0) -> None:
        self.now = start_date
        self.investments = {}
        self.indicator_data = {}
        self.strat_hist = {}
        self.interval = Utils.convert_interval(timeframe)
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.cash = cash
        self.initial_cash = cash
        self.strategy = strategy

    def __create_investment(self, symbol) -> None:
        self.investments[symbol] = Investment(symbol, self.timeframe)

    def buy(self, symbol, amount) -> bool:
        if amount > self.cash:
            warn(f"Attempted to buy {amount} of {symbol} with only {self.cash} cash")
            return False
            
        if symbol not in self.investments:
            self.__create_investment(symbol)

        self.investments[symbol].buy(self.now, amount)
        self.cash -= amount
        
        return True

    def sell(self, symbol, amount) -> bool:
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

    def get_equity(self) -> float:
        return sum(investment.get_equity(self.now) for investment in self.investments.values())

    def make_transactions(self, transactions) -> None:
        for symbol, amount in transactions.items():
            if amount > 0:
                self.buy(symbol, amount)
            else:
                self.sell(symbol, -amount)

    def plot(self, plot_assets=False, plot_indicators=False) -> None:
        plt.plot(self.strat_hist.keys(), self.strat_hist.values(), label=self.strategy.label)

        if plot_assets or plot_indicators:
            for symbol, investment in self.investments.items():
                asset = investment.asset
                shares = self.initial_cash / asset.get_price_by_date(self.start_date)

                if plot_assets:
                    asset.plot(shares=shares, show=False)

                if plot_indicators:
                    for label, data in self.indicator_data[symbol].items():
                        (data * shares).plot(show=False, label=f"{symbol} {label}")

        Utils.show_plot()

    def get_return(self) -> None:
        return (self.get_equity() + self.cash) / self.initial_cash

    def get_alpha(self) -> float:
        if len(self.investments) > 1:
            raise Exception("Alpha only makes sense with one asset")
        return self.get_return() / list(self.investments.values())[0].asset.lump_sum()

    def run(self) -> None:
        self.__create_strategy_data()
        self.__run()

    def __create_strategy_data(self) -> None:
        for symbol in self.strategy.symbols:
            self.__create_investment(symbol)
            self.indicator_data[symbol] = {}
            for indicator in self.strategy.indicators:
                historical_data = indicator.create_indicator(self.investments[symbol].asset)
                self.indicator_data[symbol][historical_data.label] = historical_data

    def __run(self) -> None:
        self.now = self.start_date
        while self.now <= self.end_date:
            self.make_transactions(self.strategy.get_transactions(self))
            self.strat_hist[self.now] = self.get_equity() + self.cash
            self.now += self.interval
        self.now = self.end_date
