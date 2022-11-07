from finance.Asset import Asset
from finance.CoinAPI import CoinAPI
from finance.HistoricalData import HistoricalData
from finance import Utils

import numpy as np
import pandas as pd

class Currency(Asset):
    def __init__(self, symbol, timeframe="1DAY", start_date=None, end_date=None, limit=10000):
        self.limit = limit

        if not start_date:
            start_date = np.datetime64(CoinAPI.get_start_date(symbol))

        super().__init__(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)

    def __create_historical_data(self, ohlcv, price_type) -> HistoricalData:
        return HistoricalData(
            values=ohlcv[price_type].values,
            dates=ohlcv["time_period_start"].to_numpy(Utils.DATETIME_TYPE),
            start_date=self.start_date,
            interval=self.interval
        )

    def get_ohlcv(self) -> None:
        json = CoinAPI.get_ohlcv(self.symbol, self.timeframe, self.start_date, self.end_date, self.limit)
        ohlcv = pd.read_json(json)

        self.start_date = np.datetime64(ohlcv["time_period_start"][0])
        self.end_date = np.datetime64(ohlcv["time_period_start"][len(ohlcv) - 1])

        self.open = self.__create_historical_data(ohlcv, "price_open")
        self.close = self.__create_historical_data(ohlcv, "price_close")
        self.high = self.__create_historical_data(ohlcv, "price_high")
        self.low = self.__create_historical_data(ohlcv, "price_low")
        self.volume = self.__create_historical_data(ohlcv, "volume_traded")
