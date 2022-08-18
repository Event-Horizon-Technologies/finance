from HistoricalData import HistoricalData
import numpy as np

def __create_price_indicator(asset, values, label=None):
    return HistoricalData(values=values, interval=asset.prices.interval, end_date=asset.prices.end_date, label=label)

def get_sma_prices(asset, period=200):
    """Returns values of Simple Moving Average for a specific period"""
    cumsum = asset.prices.values.cumsum()
    values = np.append(cumsum[period - 1], cumsum[period:] - cumsum[:-period]) / period
    return __create_price_indicator(asset, values, "SMA")

def get_ema_prices(asset, period=200):
    """Returns values of Exponential Moving Average for a specific period"""
    k = 2.0 / (period + 1)
    values = np.frompyfunc(lambda x, y: (1-k)*x + k*y, 2, 1).accumulate(asset.prices.values)
    return __create_price_indicator(asset, values, "EMA")

