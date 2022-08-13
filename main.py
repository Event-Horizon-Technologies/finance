from Stock import Stock

stock = Stock("SPY")
stock.get_SMA_prices()
stock.get_EMA_prices()
print(stock.dollar_cost_average(30))
print(stock.lump_sum())
stock.plot()
