from finance.Asset import Asset
from finance.Currency import Currency
from finance.Stock import Stock

def create_asset(symbol, timeframe="1d", start_date=None, end_date=None) -> Asset:
    if symbol.endswith("-USD"):
        return Currency(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)
    return Stock(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)
