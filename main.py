#!/usr/bin/python
from finance import Indicators, Simulator, Strategy, Asset, Utils

import numpy as np
import sys

def main(argv):
    symbol    = argv[0] if len(argv) > 0 else "BTC-USD"
    timeframe = argv[1] if len(argv) > 1 else "1d"

    asset = Asset(symbol, timeframe=timeframe)

    start = asset.close.start_date
    end = asset.close.end_date - 2 * asset.close.interval

    cash = asset.get_price_by_date(start)

    s = Simulator(start_date=start, end_date=end, timeframe=timeframe, cash=cash)
    s.run(Strategy.PSAR_EMA(symbol))
    s.plot(plot_assets=True)

    print(s.get_alpha())


if __name__ == "__main__":
    main(sys.argv[1:])
