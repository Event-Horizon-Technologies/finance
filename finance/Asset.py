from finance.HistoricalData import create_hd_from_series, HistoricalData
from finance import Utils

import numba as nb
import numpy as np
import yfinance as yf

def create_asset(symbol, history=None, timeframe="1d", start_date=Utils.MIN_DATETIME,
                 end_date=Utils.MIN_DATETIME, auto_adjust=True):
    if history is None:
        length = Utils.MAX[timeframe]
        history = yf.Ticker(symbol).history(interval=timeframe, period=length, auto_adjust=auto_adjust)

    interval = Utils.INTERVALS[timeframe]

    # the yfinance API can have bad data in the last row of history for some reason, thus the '[:-1]'
    open  = create_hd_from_series(history["Open" ][:-1], start_date=start_date, end_date=end_date, interval=interval)
    close = create_hd_from_series(history["Close"][:-1], start_date=start_date, end_date=end_date, interval=interval)
    high  = create_hd_from_series(history["High" ][:-1], start_date=start_date, end_date=end_date, interval=interval)
    low   = create_hd_from_series(history["Low"  ][:-1], start_date=start_date, end_date=end_date, interval=interval)

    return Asset(symbol, open, close, high, low)


spec = [
    ("symbol", nb.types.unicode_type),
    ("start_date", Utils.NB_DATETIME),
    ("end_date", Utils.NB_DATETIME),
    ("interval", Utils.NB_TIMEDELTA)
]

@nb.experimental.jitclass(spec)
class Asset:
    open: HistoricalData
    close: HistoricalData
    high: HistoricalData
    low: HistoricalData

    def __init__(self, symbol, open, close, high, low):
        self.symbol = symbol
        self.open = open; self.close = close; self.high = high; self.low = low
        self.start_date = self.close.start_date; self.end_date = self.close.end_date; self.interval = self.close.interval

    def get_price_by_date(self, date):
        return self.close.get_val_by_date(date)

    def dollar_cost_average(self, period):
        return (self.close.values[-1] / self.close.values[::period]).mean()

    def lump_sum(self):
        return self.close.values[-1] / self.close.values[0]

    def plot(self, shares=1, show=True):
        (self.close * shares).plot(label=self.symbol, show=show)
