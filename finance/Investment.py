from finance.Crypto import Crypto
from finance import Utils

class Investment:
    def __init__(self, symbol, timeframe):
        if Utils.is_crypto(symbol):
            self.asset = Crypto(symbol=symbol, timeframe=timeframe)
        else:
            # TODO: Use Stock Class
            pass
        self.quantity = 0.0
        self.fee = 0.00075

    def buy(self, date, amount):
        self.quantity += (1.0 - self.fee) * amount / self.asset.get_price_by_date(date)

    def sell(self, date, amount):
        self.quantity -= (1.0 + self.fee) * amount / self.asset.get_price_by_date(date)

    def get_equity(self, date):
        return self.quantity * self.asset.get_price_by_date(date)
