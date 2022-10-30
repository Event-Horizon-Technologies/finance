from finance.Static import Static
from finance import Utils

import json
import numpy as np
import requests
from pathlib import Path

API_KEY = "860A3E2F-665F-4C09-B37B-FEA28D5847DB"
HEADERS = {"X-CoinAPI-Key": API_KEY}
URL_BASE = "https://rest.coinapi.io/v1"
EXCHANGE = "COINBASE"
SYMBOLS_PATH = Path(__file__).parent.joinpath("data/coinapi/symbols.json")

class CoinAPI(Static):
  @staticmethod
  def convert_timeframe(timeframe) -> str:
    match timeframe:
      case "1d": return "1DAY"
      case "1h": return "1HRS"
      case "5m": return "5MIN"
      case "1m": return "1MIN"
    return timeframe

  @staticmethod
  def get_start_date(symbol):
    symbol = symbol.replace("-USD", "")
    with open(SYMBOLS_PATH) as f:
      for asset in (asset for asset in json.loads(f.read()) if asset["symbol_id"] == f"{EXCHANGE}_SPOT_{symbol}_USD"):
        return asset["data_start"]

  @staticmethod
  def get_ohlcv(symbol, timeframe, start_date, end_date=None, limit=None) -> str:
    symbol = symbol.replace("-USD", "")
    timeframe = CoinAPI.convert_timeframe(timeframe)
    if end_date:
      # We use an inclusive interval for dates but theirs is exclusive, need to add 1
      end_date = np.datetime64(end_date) + Utils.convert_interval(timeframe)

    url = f"{URL_BASE}/ohlcv/{EXCHANGE}_SPOT_{symbol}_USD/history?period_id={timeframe}&time_start={start_date}"
    if end_date:
      url += f"&time_end={end_date}"
    if limit:
      url += f"&limit={limit}"

    return requests.get(url, headers=HEADERS).text

  @staticmethod
  def get_assets() -> str:
    return requests.get(f"{URL_BASE}/assets", headers=HEADERS).text

  @staticmethod
  def get_symbols() -> str:
    return requests.get(f"{URL_BASE}/symbols", headers=HEADERS).text
