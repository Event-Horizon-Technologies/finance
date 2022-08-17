from datetime import datetime
from Simulator import Simulator

def strategy(simulator):
    return {"SPY": simulator.cash} if simulator.now == simulator.start_date else {}

start = datetime.strptime("1994-01-01", "%Y-%m-%d")
end = datetime.strptime("2022-01-01", "%Y-%m-%d")

s = Simulator(start_date=start, end_date=end, cash=100)
percent = s.run(strategy)
print(percent)