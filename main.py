from datetime import datetime
from Simulator import Simulator
from Strategy import *
import Indicators
from Asset import Asset
import matplotlib.pyplot as plt
from pytz import UTC

SYMBOL = "BTC-USD"
TIMEFRAME = "1d"


asset = Asset(SYMBOL, timeframe=TIMEFRAME)
data = asset.prices

start = asset.prices.start_date
end = asset.prices.end_date - 2 * asset.prices.interval

# start = datetime.strptime("2021-01-01", "%Y-%m-%d").replace(tzinfo=UTC)
# end = datetime.strptime("2022-01-01", "%Y-%m-%d").replace(tzinfo=UTC)

cash = asset.get_price_by_date(start)

s = Simulator(start_date=start, end_date=end, timeframe=TIMEFRAME, cash=cash)
mult = s.run(MeanReversion(SYMBOL))
s.plot(plot_assets=True, plot_indicators=True)

# print(mult)

