import numba as nb
import numpy as np
from finance import create_asset, Utils, create_investment, plot, Indicators, HistoricalData, Strategy

# asset = create_asset(symbol="SPY", timeframe="1d")
# psar = Indicators.PSAR().create_indicator(asset)
# plot(psar)

bah = Strategy.BuyAndHold()
