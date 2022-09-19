from finance import Indicators, Utils
from finance.HistoricalData import HistoricalData

import numba as nb
import numpy as np
import numpy.typing as npt
from datetime import datetime

MIN_DATETIME = np.datetime64(datetime.min, Utils.DATETIME_SYMBOL)
NP_DATETIME = type(np.array([MIN_DATETIME]))

# @nb.experimental.jitclass([("label", nb.types.unicode_type), ("symbols", nb.types.unicode_type), ("indicators", nb.experimental.jitclass.base.HistoricalData[:])])
@nb.experimental.jitclass([("label", nb.types.unicode_type), ("symbols", nb.types.unicode_type[:])])
class BuyAndHold:
    indicators: HistoricalData

    def __init__(self, symbol="SPY"):
        self.label = "BuyAndHold"
        self.symbols = np.empty()
        # self.indicators =

    # def get_transactions(self, simulator):
    #     return {self.symbols[0]: simulator.cash} if simulator.now == simulator.start_date else {}

# class MeanReversion(Strategy):
#     def __init__(self, symbol="SPY", buy_thresh=0.95, sell_thresh=3):
#         super().__init__([symbol], [Indicators.EMA()])
#         self.buy_thresh = buy_thresh
#         self.sell_thresh = sell_thresh
#         self.ind_label = "EMA"
#
#     def get_transactions(self, simulator):
#         date = simulator.now
#         ema_val = simulator.indicator_data[self.symbols[0]][self.ind_label].get_val_by_date(date)
#         price = simulator.investments[self.symbols[0]].asset.get_price_by_date(date)
#         equity = simulator.investments[self.symbols[0]].get_equity(date)
#
#         if price <= self.buy_thresh * ema_val and simulator.cash > 0:
#             return {self.symbols[0]: simulator.cash}
#
#         if price >= self.sell_thresh * ema_val and equity > 0:
#             return {self.symbols[0]: -equity}
#
#         return {}
#
# class PSAR_EMA(Strategy):
#     def __init__(self, symbol="SPY", short_period=20, long_period=40):
#         self.short_period, self.long_period = sorted((short_period, long_period))
#         super().__init__([symbol], [
#             Indicators.PSAR(),
#             Indicators.EMA(self.short_period_label, short_period),
#             Indicators.EMA(self.long_period_label, long_period)
#         ])
#
#     @property
#     def short_period_label(self):
#         return f"EMA-{self.short_period}"
#
#     @property
#     def long_period_label(self):
#         return f"EMA-{self.long_period}"
#
#     @property
#     def psar_label(self):
#         return "PSAR"
#
#     def __get_indicator_value(self, label):
#         return self.simulator.indicator_data[self.symbols[0]][label].get_val_by_date(self.simulator.now)
#
#     def __get_asset_value(self):
#         return self.simulator.investments[self.symbols[0]].asset.get_price_by_date(self.simulator.now)
#
#     def get_transactions(self, simulator):
#         self.simulator = simulator
#         equity = simulator.investments[self.symbols[0]].get_equity(simulator.now)
#
#         if (simulator.cash > 0 and self.__get_indicator_value(self.psar_label) < self.__get_asset_value() and
#                 self.__get_indicator_value(self.short_period_label) > self.__get_indicator_value(self.long_period_label)):
#             return {self.symbols[0]: simulator.cash}
#
#         if (equity > 0 and self.__get_indicator_value(self.psar_label) > self.__get_asset_value() and
#                 self.__get_indicator_value(self.short_period_label) < self.__get_indicator_value(self.long_period_label)):
#             return {self.symbols[0]: -equity}
#
#         return {}
