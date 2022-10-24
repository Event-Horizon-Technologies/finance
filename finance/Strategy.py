from finance import Indicators

from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, symbols=None, indicators=None) -> None:
        self.symbols = symbols
        self.indicators = indicators
        self.simulator = None

    @abstractmethod
    def get_transactions(self, simulator) -> dict[str, float]: pass

    @property
    def label(self):
        return self.__class__.__name__

class BuyAndHold(Strategy):
    def __init__(self, symbol="SPY") -> None:
        super().__init__([symbol], [])

    def get_transactions(self, simulator) -> dict[str, float]:
        return {self.symbols[0]: simulator.cash} if simulator.now == simulator.start_date else {}

class MeanReversion(Strategy):
    def __init__(self, symbol="SPY", buy_thresh=0.95, sell_thresh=3) -> None:
        super().__init__([symbol], [Indicators.EMA()])
        self.buy_thresh = buy_thresh
        self.sell_thresh = sell_thresh
        self.ind_label = "EMA"

    def get_transactions(self, simulator) -> dict[str, float]:
        date = simulator.now
        ema_val = simulator.indicator_data[self.symbols[0]][self.ind_label].get_val_by_date(date)
        price = simulator.investments[self.symbols[0]].asset.get_price_by_date(date)
        equity = simulator.investments[self.symbols[0]].get_equity(date)

        if price <= self.buy_thresh * ema_val and simulator.cash > 0:
            return {self.symbols[0]: simulator.cash}

        if price >= self.sell_thresh * ema_val and equity > 0:
            return {self.symbols[0]: -equity}

        return {}

class PSAR_EMA(Strategy):
    def __init__(self, symbol="SPY", short_period=20, long_period=40) -> None:
        self.short_period, self.long_period = sorted((short_period, long_period))
        super().__init__([symbol], [
            Indicators.PSAR(),
            Indicators.EMA(self.short_period_label, short_period),
            Indicators.EMA(self.long_period_label, long_period)
        ])

    @property
    def short_period_label(self) -> str:
        return f"EMA-{self.short_period}"

    @property
    def long_period_label(self) -> str:
        return f"EMA-{self.long_period}"

    @property
    def psar_label(self) -> str:
        return "PSAR"

    def __get_indicator_value(self, label) -> float:
        return self.simulator.indicator_data[self.symbols[0]][label].get_val_by_date(self.simulator.now)

    def __get_asset_value(self) -> float:
        return self.simulator.investments[self.symbols[0]].asset.get_price_by_date(self.simulator.now)

    def get_transactions(self, simulator) -> dict[str, float]:
        self.simulator = simulator
        equity = simulator.investments[self.symbols[0]].get_equity(simulator.now)

        if (simulator.cash > 0 and self.__get_indicator_value(self.psar_label) < self.__get_asset_value() and 
                self.__get_indicator_value(self.short_period_label) > self.__get_indicator_value(self.long_period_label)):
            return {self.symbols[0]: simulator.cash}

        if (equity > 0 and self.__get_indicator_value(self.psar_label) > self.__get_asset_value() and 
                self.__get_indicator_value(self.short_period_label) < self.__get_indicator_value(self.long_period_label)):
            return {self.symbols[0]: -equity}

        return {}
