from Asset import Asset

class Investment:
    def __init__(self, ticker, timeframe, length):
      self.asset = Asset(ticker, timeframe, length)
      self.equity = None
      self.shares = None
      self.average_cost = None
      self.diversity = None

    def update_diversification(self, total_equity):
        self.diversity = total_equity / self.equity

    def get_equity(self):
        return self.equity

    def buy(self):
        pass

    def sell(self):
        pass
