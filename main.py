from datetime import datetime
from Simulator import Simulator
from Strategy import Strategy
import Indicators
from Asset import Asset
import matplotlib.pyplot as plt
from pytz import UTC

SYMBOL = "BTC-USD"
TIMEFRAME = "1d"

class HoldSpy(Strategy):
    def __init__(self):
        super().__init__([SYMBOL], [Indicators.get_ema_prices])

    def strategy(self, simulator):
        return {SYMBOL: simulator.cash} if simulator.now == simulator.start_date else {}
    
class MeanReversion(Strategy):
    def __init__(self):
        self.buy_thresh = 0.95
        self.sell_thresh = 3
        self.ind_symbol = "EMA"
        super().__init__([SYMBOL], [Indicators.get_ema_prices])

    def strategy(self, simulator):
        date = simulator.now
        ema_val = simulator.indicators[self.symbols[0]][self.ind_symbol].get_val_by_date(date)
        price = simulator.investments[self.symbols[0]].asset.get_price_by_date(date)
        equity = simulator.investments[self.symbols[0]].get_equity(date)

        if price <= self.buy_thresh * ema_val and simulator.cash > 0:
            return {self.symbols[0]: simulator.cash}

        if price >= self.sell_thresh * ema_val and equity > 0:
            return {self.symbols[0]: -equity}

        return {}


asset = Asset(SYMBOL, timeframe=TIMEFRAME)

start = asset.prices.start_date
end = asset.prices.end_date - asset.prices.interval

# start = datetime.strptime("2021-01-01", "%Y-%m-%d").replace(tzinfo=UTC)
# end = datetime.strptime("2022-01-01", "%Y-%m-%d").replace(tzinfo=UTC)

cash = asset.get_price_by_date(start)

s = Simulator(start_date=start, end_date=end, timeframe=TIMEFRAME, cash=cash)
mult = s.run(MeanReversion())

asset.prices.plot()
plt.legend(loc='best', prop={'size': 20})
plt.show()

print(mult)
