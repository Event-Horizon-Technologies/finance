from Asset import Asset

class Investment:
    def __init__(self, symbol, timeframe, length):
      self.asset = Asset(symbol, timeframe, length)
      self.equity = None
      self.shares = None
      self.average_cost = None
      self.diversity = None

    def update_diversification(self, total_equity):
        self.diversity = self.equity / total_equity

    def get_equity(self):
        return self.equity

    def buy(self):
        pass

    def sell(self):
        pass
