from finance import Utils

from abc import ABC, abstractmethod

class Asset(ABC):
    def __init__(self, symbol, timeframe="1d", start_date=None, end_date=None) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.start_date = start_date
        self.end_date = end_date
        self.interval = Utils.convert_interval(timeframe)
        self.open = self.close = self.high = self.low = self.volume = None

        self.get_ohlcv()

        self.start_date, self.end_date = self.close.start_date, self.close.end_date

    @abstractmethod
    def get_ohlcv(self) -> None: pass

    def get_price_by_date(self, date) -> float:
        return self.close.get_val_by_date(date)

    def dollar_cost_average(self, period) -> float:
        return (self.close.values[-1] / self.close.values[::period]).mean()

    def lump_sum(self) -> float:
        return self.close.values[-1] / self.close.values[0]

    def plot(self, shares=1, show=True) -> None:
        (self.close * shares).plot(label=self.symbol, show=show)
