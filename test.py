import numba as nb
import numpy as np
from finance import create_asset
from finance import Utils, create_investment, plot
from finance import Indicators

asset = create_asset(symbol="SPY", timeframe="1d")
psar = Indicators.PSAR().create_indicator(asset)
plot(psar)
