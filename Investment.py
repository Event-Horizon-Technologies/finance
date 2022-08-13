from Asset import Asset

class Investment:
    def __init__(self, ticker, timeframe, length):
      self.asset = Asset(ticker, timeframe, length)

