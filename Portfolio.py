from Investment import Investment

class Portfolio:
    def __init__(self):
        self.investments= {}
        self.timeframe = None
        self.length = None
        self.total_equity = None

    def buy_asset(self, ticker, amount):
        if ticker not in self.investments:
            self.investments[ticker] = Investment(ticker, self.timeframe, self.length)


    def update_diversifications(self):
        for investment in self.investments.values():
            investment.update_diversification(self.total_equity)
            
    def set_timeframe(self, timeframe):
        self.timeframe = timeframe