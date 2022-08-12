from Asset import Asset

class Portfolio:
    def __init__(self):
        self.assets = {}
        self.timeframe = None
        self.length = None
    
    def buy_asset(self, ticker, amount):
        owned = self.assets.get(ticker)
        if not owned:
            self.assets[ticker] = Asset(ticker, self.timeframe, self.length)
        
        
    def get_asset(self, ticker):
        return self.assets[ticker]

    def set_timeframe(self, timeframe):
        self.timeframe = timeframe