import numba as nb
import numpy as np
from finance import create_asset
from finance import Utils, create_investment, plot

investment = create_investment(symbol="SPY", timeframe="1d", quantity=1.0)
print(investment.asset.close.values)
plot(investment)