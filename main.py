from Stock import Stock

# stock = Stock("ETHUSD")
stock = Stock("SPY", timeframe="1h", length="2y")
stock.plot()

