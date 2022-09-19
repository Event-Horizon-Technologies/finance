#!/usr/bin/python
from finance import Indicators, Simulator, Strategy, Asset, Utils, HistoricalData, create_asset, Plotting

import numba
import numpy as np
import sys

def main(argv):
    symbol    = argv[0] if len(argv) > 0 else "BTC-USD"
    timeframe = argv[1] if len(argv) > 1 else "1d"

    asset = create_asset(symbol, timeframe=timeframe)

    start = asset.close.start_date
    end = asset.close.end_date

    cash = asset.get_price_by_date(start)

    s = Simulator(strategy=Strategy.BuyAndHold(symbol), start_date=start, end_date=end, timeframe=timeframe, cash=cash)
    from time import time

    # sum = 0
    # n = 20
    # for i in range(n):
    #     start = time()
    #     s.run()
    #     sum += time() - start
    # print(sum / n)

    s.run()
    Plotting.plot(s, plot_assets=True)
    #
    # print(s.get_alpha())


if __name__ == "__main__":
    main(sys.argv[1:])
