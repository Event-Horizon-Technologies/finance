from Stock import Stock

# stock = Stock("ETHUSD")
stock = Stock("ETHUSD", timeframe="D", update=True)

stock.plot()



