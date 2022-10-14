from finance import Asset
from test.TestBaseClass import TestBaseClass
from finance import Utils

import numpy as np

class TestAsset(TestBaseClass):
    def __test_asset(self, symbol, timeframe, start_date_str, end_date_str):
        start_date = np.datetime64(start_date_str, Utils.DATETIME_SYMBOL)
        end_date = np.datetime64(end_date_str, Utils.DATETIME_SYMBOL)
        history = self.get_pickle("history") if self.IN_TESTING_MODE else None
        asset = Asset(symbol=symbol, history=history, timeframe=timeframe, start_date=start_date, end_date=end_date)

        if self.IN_PICKLE_GENERATION_MODE:
            self.store_pickle("history", asset.history)

        self.run(open=asset.open, close=asset.close, high=asset.high, low=asset.low)

    def test_btc_1d(self):
        self.__test_asset(symbol="BTC-USD", timeframe="1day", start_date_str="2014-09-18", end_date_str="2022-09-06")

    def test_btc_1h(self):
        self.__test_asset(symbol="BTC-USD", timeframe="1h", start_date_str="2021-09-06", end_date_str="2022-09-06")

    def test_spy_1d(self):
        self.__test_asset(symbol="SPY", timeframe="1day", start_date_str="1993-01-30", end_date_str="2022-09-06")
