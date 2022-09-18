from finance.Asset import Asset
from finance import Utils

import numba as nb

def create_investment(symbol, timeframe, quantity=0.0, fee=0.00075):
    asset = Asset(symbol=symbol, timeframe=timeframe)
    return Investment(asset.open.values, asset.close.values, asset.high.values, asset.low.values,
                      asset.start_date, asset.end_date, asset.interval, quantity, fee)


spec = [
    ("open", nb.float64[:]),
    ("close", nb.float64[:]),
    ("high", nb.float64[:]),
    ("low", nb.float64[:]),
    ("start_date", Utils.NB_DATETIME),
    ("end_date", Utils.NB_DATETIME),
    ("interval", Utils.NB_TIMEDELTA),
    ("quantity", nb.float64),
    ("fee", nb.float64)
]

@nb.experimental.jitclass(spec)
class Investment:
    def __init__(self, open, close, high, low, start_date, end_date, interval, quantity, fee):
        self.open = open; self.close = close; self.high = high; self.low = low; self.start_date = start_date
        self.end_date = end_date; self.interval = interval; self.quantity = quantity; self.fee = fee

    def buy(self, date, amount):
        self.quantity += (1.0 - self.fee) * amount / self.get_price_by_date(date)

    def sell(self, date, amount):
        self.quantity -= (1.0 + self.fee) * amount / self.get_price_by_date(date)

    def get_equity(self, date):
        return self.quantity * self.get_price_by_date(date)
    
    def in_bounds(self, date):
        return self.start_date <= date <= self.end_date
    
    def get_price_by_date(self, date):
        if not self.in_bounds(date):
            raise Exception(f"Date {date} is out of bounds")
        return self.close[round((date - self.start_date) / self.interval)]
