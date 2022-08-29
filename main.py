#!/usr/bin/python

from datetime import datetime, timedelta
from Simulator import Simulator
from Strategy import *
import Indicators
from Asset import Asset
from pytz import UTC
import sys

def main(argv):
    symbol    = argv[0] if len(argv) > 0 else "NVDA"
    timeframe = argv[1] if len(argv) > 1 else "5m"

    asset = Asset(symbol, timeframe=timeframe)

    start = asset.close.start_date
    end = asset.close.end_date - 2 * asset.close.interval

    # start = datetime.strptime("2021-01-01", "%Y-%m-%d").replace(tzinfo=UTC)
    # end = datetime.strptime("2022-01-01", "%Y-%m-%d").replace(tzinfo=UTC)

    cash = asset.get_price_by_date(start)

    s = Simulator(start_date=start, end_date=end, timeframe=timeframe, cash=cash)
    s.run(PSAR_EMA(symbol))
    s.plot(plot_assets=True)

    print(s.get_alpha())


if __name__ == "__main__":
    main(sys.argv[1:])
