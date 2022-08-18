from datetime import datetime
from Simulator import Simulator
from Strategy import Strategy
from Indicators import *
from Asset import Asset

class HoldSpy(Strategy):
    def __init__(self):
        super().__init__(["BTC-USD"], [get_ema_prices])

    def strategy(self, simulator):
        return {"BTC-USD": simulator.cash} if simulator.now == simulator.start_date else {}


start = datetime.strptime("2015-05-01", "%Y-%m-%d")
end = datetime.strptime("2022-01-01", "%Y-%m-%d")

s = Simulator(start_date=start, end_date=end, cash=1)
mult = s.run(HoldSpy())
print(mult)

