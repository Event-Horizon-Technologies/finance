from Investment import Investment

class Portfolio:
    def __init__(self):
        self.investments= {}
        self.timeframe = None
        self.length = None
    
    def buy_asset(self, ticker, amount):
        if ticker not in self.investments:
            self.investments[ticker] = Investment(ticker, self.timeframe, self.length)
        pass

    def set_timeframe(self, timeframe):
        self.timeframe = timeframe