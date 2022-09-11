from finance import Asset
from test.TestBaseClass import TestBaseClass
from finance import Utils

import numpy as np

class TestAsset(TestBaseClass):
    def test_btc_1d(self):
        start_date = np.datetime64("2014-09-17", Utils.DATETIME_TYPE)
        end_date = np.datetime64("2022-09-06", Utils.DATETIME_TYPE)
        asset = Asset(symbol="BTC-USD", timeframe="1d", start_date=start_date, end_date=end_date)

        self.run(open=asset.open, close=asset.close, high=asset.high, low=asset.low)

    def test_spy_1d(self):
        start_date = np.datetime64("2014-09-17", Utils.DATETIME_TYPE)
        end_date = np.datetime64("2022-09-06", Utils.DATETIME_TYPE)
        asset = Asset(symbol="SPY", timeframe="1d", start_date=start_date, end_date=end_date)

        self.run(open=asset.open, close=asset.close, high=asset.high, low=asset.low)

