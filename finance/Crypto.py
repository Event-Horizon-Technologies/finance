from finance.Asset import Asset
from finance.CoinAPI import CoinAPI
from finance.HistoricalData import HistoricalData
from finance import Utils

import numpy as np
import pandas as pd

class Crypto(Asset):
    def __init__(self, symbol, timeframe="1DAY", start_date=None, end_date=None, limit=100):
        self.limit = limit

        if not start_date:
            start_date = np.datetime64(CoinAPI.get_start_date(symbol))

        # interval = Utils.convert_interval(timeframe)
        # end_date_limit = start_date + (limit - 1) * interval
        # if not end_date or end_date > end_date_limit:
        #     end_date = end_date_limit

        super().__init__(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)

    def get_ohlcv(self) -> None:
        json = CoinAPI.get_ohlcv(self.symbol, self.timeframe, self.start_date, self.end_date, self.limit)
        ohlcv = pd.read_json(json)

        # TODO: There's fucking missing dates, we have to do the interpolation..
        self.start_date = np.datetime64(ohlcv["time_period_start"][0])
        self.end_date = np.datetime64(ohlcv["time_period_start"][len(ohlcv) - 1])

        self.open = HistoricalData(values=ohlcv["price_open"].values, start_date=self.start_date, interval=self.interval)
        self.close = HistoricalData(values=ohlcv["price_close"].values, start_date=self.start_date, interval=self.interval)
        self.high = HistoricalData(values=ohlcv["price_high"].values, start_date=self.start_date, interval=self.interval)
        self.low = HistoricalData(values=ohlcv["price_low"].values, start_date=self.start_date, interval=self.interval)
        self.volume = HistoricalData(values=ohlcv["volume_traded"].values, start_date=self.start_date, interval=self.interval)
