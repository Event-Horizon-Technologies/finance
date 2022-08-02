from Stock import Stock

stock = Stock("BTCUSD")
# stock = Stock("SPY")
stock.plot()

# Time is in reverse order
for i in stock.prices.__reversed__():
    print(i)