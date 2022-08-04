from Stock import Stock

# stock = Stock("ETHUSD")
stock = Stock("SPY")

size = len(stock.prices.values())

winning_periods = 0.0

lump_sum = stock.lump_sum()

for i in range(1, size // 2):
    dca = stock.dollar_cost_average(i)
    if dca > lump_sum:
        winning_periods += 1

win_ratio = winning_periods / (size // 2)

print("Percent Win: " + str(100 * win_ratio))



