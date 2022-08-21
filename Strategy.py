from abc import ABC, abstractmethod
import Indicators

class Strategy(ABC):
    def __init__(self, symbols=None, indicators=None):
        self.symbols = symbols
        self.indicators = indicators

    @abstractmethod
    def strategy(self, simulator):
        return {}

class BuyAndHold(Strategy):
    def __init__(self, symbol="SPY"):
        super().__init__([symbol], [])

    def strategy(self, simulator):
        return {self.symbols[0]: simulator.cash} if simulator.now == simulator.start_date else {}

class MeanReversion(Strategy):
    def __init__(self, symbol="SPY", buy_thresh=0.95, sell_thresh=3):
        super().__init__([symbol], [Indicators.EMA()])
        self.buy_thresh = buy_thresh
        self.sell_thresh = sell_thresh
        self.label = self.indicators[0].label

    def strategy(self, simulator):
        date = simulator.now
        ema_val = simulator.indicators[self.symbols[0]][self.label].get_val_by_date(date)
        price = simulator.investments[self.symbols[0]].asset.get_price_by_date(date)
        equity = simulator.investments[self.symbols[0]].get_equity(date)

        if price <= self.buy_thresh * ema_val and simulator.cash > 0:
            return {self.symbols[0]: simulator.cash}

        if price >= self.sell_thresh * ema_val and equity > 0:
            return {self.symbols[0]: -equity}

        return {}
