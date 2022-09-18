import numba as nb
import numpy as np
from finance import create_asset
from finance import Utils

asset = create_asset(symbol="SPY", timeframe="1d")
print(asset.close.values)
# asset.plot()