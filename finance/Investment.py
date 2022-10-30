from finance.Asset import Asset

class Investment:
  def __init__(self, symbol, timeframe) -> None:
    self.asset = Asset(symbol=symbol, timeframe=timeframe)
    self.quantity = 0.0
    self.fee = 0.00075

  def buy(self, date, amount) -> None:
    self.quantity += (1.0 - self.fee) * amount / self.asset.get_price_by_date(date)

  def sell(self, date, amount) -> None:
    self.quantity -= (1.0 + self.fee) * amount / self.asset.get_price_by_date(date)

  def get_equity(self, date) -> float:
    return self.quantity * self.asset.get_price_by_date(date)
