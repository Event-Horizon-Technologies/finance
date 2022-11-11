from finance import Indicators
from finance.HistoricalData import HistoricalData

from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, symbols=None) -> None:
        self.symbols = symbols
        self.simulator = None

    def attach_simulator(self, simulator) -> None:
        self.simulator = simulator
        self.on_simulator_attached()

    @abstractmethod
    def on_simulator_attached(self) -> None: pass

    @abstractmethod
    def get_transactions(self) -> dict[str, float]: pass

    @property
    def label(self) -> str: return self.__class__.__name__

class BuyAndHold(Strategy):
    def __init__(self, symbol="SPY") -> None:
        super().__init__([symbol])
        self.symbol = symbol

    def on_simulator_attached(self) -> None: pass

    def get_transactions(self) -> dict[str, float]:
        return {self.symbol: self.simulator.cash} if self.simulator.now == self.simulator.start_date else {}

class MeanReversion(Strategy):
    def __init__(self, symbol="SPY", buy_thresh=0.95, sell_thresh=3) -> None:
        super().__init__([symbol])
        self.symbol = symbol
        self.buy_thresh = buy_thresh
        self.sell_thresh = sell_thresh
        self.ema = None

    def on_simulator_attached(self) -> None:
        self.ema = Indicators.EMA().create_indicator(self.simulator.asset)

    def get_transactions(self) -> dict[str, float]:
        investment = self.simulator.investments[self.symbol]
        asset = investment.asset

        date = self.simulator.now
        ema_val = self.ema[date]
        price = asset.close[date]
        equity = investment.get_equity(date)

        if price <= self.buy_thresh * ema_val and self.simulator.cash > 0:
            return {self.symbol: self.simulator.cash}

        if price >= self.sell_thresh * ema_val and equity > 0:
            return {self.symbol: -equity}

        return {}

class PSAR_EMA(Strategy):
    def __init__(self, symbol="SPY", short_period=20, long_period=40) -> None:
        self.symbol = symbol
        self.short_period, self.long_period = sorted((short_period, long_period))
        self.psar = self.short_ema = self.long_ema = None
        super().__init__([symbol])

    def on_simulator_attached(self) -> None:
        asset = self.simulator.investments[self.symbol].asset
        self.psar = Indicators.PSAR().create_indicator(asset)
        self.short_ema = Indicators.EMA(f"EMA-{self.short_period}", self.short_period).create_indicator(asset)
        self.long_ema = Indicators.EMA(f"EMA-{self.long_period}", self.long_period).create_indicator(asset)

    def get_transactions(self) -> dict[str, float]:
        investment = self.simulator.investments[self.symbol]
        asset = investment.asset
        equity = investment.get_equity(self.simulator.now)
        now = self.simulator.now

        if self.simulator.cash > 0 and self.psar[now] < asset.close[now] and self.short_ema[now] > self.long_ema[now]:
            return {self.symbol: self.simulator.cash}

        if equity > 0 and self.psar[now] > asset.close[now] and self.short_ema[now] < self.long_ema[now]:
            return {self.symbol: -equity}

        return {}

class NeuralNetwork(Strategy):
    def __init__(self, symbols, trainer) -> None:
        super().__init__(symbols)
        self.trainer = trainer
        self.indicator_dict = None

    def __generate_indicator_data(self, symbol) -> HistoricalData:
        asset = self.simulator.investments[symbol].asset
        array = self.trainer.generate_indicator_data(asset)
        return HistoricalData(values=array, start_date=asset.start_date, end_date=asset.end_date)

    def on_simulator_attached(self) -> None:
        self.indicator_dict = {symbol: self.__generate_indicator_data(symbol) for symbol in self.symbols}

    def get_transactions(self) -> dict[str, float]:
        # assuming for now there is only one asset
        symbol = self.symbols[0]
        equity = self.simulator.investments[symbol].get_equity(self.simulator.now)
        cash = self.simulator.cash
        prediction = self.trainer.predict(self.indicator_dict[symbol][self.simulator.now], standardized=False)

        if cash > 0.0 and prediction > 0.0:
            return {symbol: cash}

        if equity > 0.0 and prediction < 0.0:
            return {symbol: -equity}

        return {}