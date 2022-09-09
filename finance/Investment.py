from Asset import Asset

class Investment:
    def __init__(self, symbol, timeframe):
        self.asset = Asset(symbol, timeframe)
        self.quantity = 0.0
        self.fee = 0.00075

    def buy(self, date, amount):
        self.quantity += (1.0 - self.fee) * amount / self.asset.get_price_by_date(date)

    def sell(self, date, amount):
        self.quantity -= (1.0 + self.fee) * amount / self.asset.get_price_by_date(date)

    def get_equity(self, date):
        return self.quantity * self.asset.get_price_by_date(date)
