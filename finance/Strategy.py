from abc import ABC, abstractmethod
import Indicators

class Strategy(ABC):
    def __init__(self, symbols=None, indicators=None):
        self.symbols = symbols
        self.indicators = indicators
        self.simulator = None

    @abstractmethod
    def strategy(self, simulator):
        pass


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
        ema_val = simulator.indicator_data[self.symbols[0]][self.label].get_val_by_date(date)
        price = simulator.investments[self.symbols[0]].asset.get_price_by_date(date)
        equity = simulator.investments[self.symbols[0]].get_equity(date)

        if price <= self.buy_thresh * ema_val and simulator.cash > 0:
            return {self.symbols[0]: simulator.cash}

        if price >= self.sell_thresh * ema_val and equity > 0:
            return {self.symbols[0]: -equity}

        return {}


class PSAR_EMA(Strategy):
    def __init__(self, symbol="SPY", short_period=20, long_period=40):
        self.short_period, self.long_period = sorted((short_period, long_period))
        super().__init__([symbol], [
            Indicators.PSAR(),
            Indicators.EMA(self.short_period_label, short_period),
            Indicators.EMA(self.long_period_label, long_period)
        ])

    @property
    def short_period_label(self):
        return f"EMA-{self.short_period}"

    @property
    def long_period_label(self):
        return f"EMA-{self.long_period}"

    def __get_indicator_value(self, label):
        return self.simulator.indicator_data[self.symbols[0]][label].get_val_by_date(self.simulator.now)

    def __get_asset_value(self):
        return self.simulator.investments[self.symbols[0]].asset.get_price_by_date(self.simulator.now)

    def strategy(self, simulator):
        self.simulator = simulator
        equity = simulator.investments[self.symbols[0]].get_equity(simulator.now)

        if not self.simulator.indicator_data[self.symbols[0]]["PSAR"].in_bounds(simulator.now):
            return {}

        if (simulator.cash > 0 and self.__get_indicator_value("PSAR") < self.__get_asset_value() and 
                self.__get_indicator_value(self.short_period_label) > self.__get_indicator_value(self.long_period_label)):
            return {self.symbols[0]: simulator.cash}

        if (equity > 0 and self.__get_indicator_value("PSAR") > self.__get_asset_value() and 
                self.__get_indicator_value(self.short_period_label) < self.__get_indicator_value(self.long_period_label)):
            return {self.symbols[0]: -equity}

        return {}
