from Asset import Asset

# stock = Stock("ETHUSD")
stock = Asset("SPY", timeframe="1h", length="2y")
stock.plot()

