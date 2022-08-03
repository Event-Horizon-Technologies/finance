from Stock import Stock

# stock = Stock("BTCUSD")
stock = Stock("SPY")
stock.get_EMA_prices()
stock.get_SMA_prices()
stock.plot()
