from finance.AlphaVantage import AlphaVantage
from finance.Asset import Asset
from finance.HistoricalData import HistoricalData
from finance import Utils

class Crypto(Asset):
    MARKET = "USD"

    def __init__(self, symbol, timeframe="1day", start_date=None, end_date=None):
        super().__init__(symbol, timeframe, start_date, end_date)

    def get_history(self):
        df = AlphaVantage.get_crypto_data(symbol=self.symbol, interval=self.timeframe, market=Crypto.MARKET)
        n = len(df)
        # Note: The API returns the latest dates first, thus the backwardness of the following code
        end_date = Utils.create_np_datetime(df.loc[0, "timestamp"])
        start_date = Utils.create_np_datetime(df.loc[n-1, "timestamp"])
        start_idx = 0
        end_idx = n

        # trim data if it goes out of bounds of self.start_date and self.end_date
        if self.end_date:
            start_idx = round((self.start_date - start_date + self.interval) / self.interval)
        if self.start_date:
            end_idx = n - round((end_date - self.end_date + self.interval) / self.interval)
        df = df[start_idx:end_idx]

        self.start_date, self.end_date = start_date, end_date

        for i, name in enumerate(["open", "close", "high", "low", "volume"]):
            setattr(self, name, HistoricalData(values=df.loc[:, df.columns[i+1]].values,
                                               start_date=start_date, end_date=end_date, interval=self.interval))
