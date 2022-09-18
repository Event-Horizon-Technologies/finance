from finance.Asset import Asset, create_asset
from finance import Utils

import numba as nb

def create_investment(symbol, timeframe, start_date=Utils.MIN_DATETIME,
                      end_date=Utils.MIN_DATETIME, quantity=0.0, fee=0.00075):
    asset = create_asset(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)
    return Investment(asset=asset, quantity=quantity, fee=fee)


spec = [
    ("quantity", nb.float64),
    ("fee", nb.float64)
]

@nb.experimental.jitclass(spec)
class Investment:
    asset: Asset

    def __init__(self, asset, quantity=0.0, fee=0.00075):
        self.asset = asset; self.quantity = quantity; self.fee = fee

    def buy(self, date, amount):
        self.quantity += (1.0 - self.fee) * amount / self.asset.get_price_by_date(date)

    def sell(self, date, amount):
        self.quantity -= (1.0 + self.fee) * amount / self.asset.get_price_by_date(date)

    def get_equity(self, date):
        return self.quantity * self.asset.get_price_by_date(date)
