from finance.create_asset import create_asset

class Investment:
    def __init__(self, symbol, timeframe) -> None:
        self.asset = create_asset(symbol=symbol, timeframe=timeframe)
        self.quantity = 0.0
        self.fee = 0.00075

    def buy(self, date, amount) -> None:
        self.quantity += (1.0 - self.fee) * amount / self.asset.close[date]

    def sell(self, date, amount) -> None:
        self.quantity -= (1.0 + self.fee) * amount / self.asset.close[date]

    def get_equity(self, date) -> float:
        return self.quantity * self.asset.close[date]
