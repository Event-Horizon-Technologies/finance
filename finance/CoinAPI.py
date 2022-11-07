from finance.Static import Static
from finance import Utils

import json
import numpy as np
import requests
from pathlib import Path

URL_BASE = "https://rest.coinapi.io/v1"
EXCHANGE = "COINBASE"
SYMBOLS_PATH = Path(__file__).parent.joinpath("data/coinapi/symbols.json")

class CoinAPI(Static):
    API_KEYS = ["860A3E2F-665F-4C09-B37B-FEA28D5847DB", "37EEFEEB-2126-4664-818F-7DF11A44594F"]
    API_KEY_IDX = 0

    @Utils.classproperty
    def HEADERS(cls) -> dict[str, str]:
        return {"X-CoinAPI-Key": cls.API_KEYS[cls.API_KEY_IDX]}

    @staticmethod
    def make_request(url, attempt=0) -> str:
        if attempt == len(CoinAPI.API_KEYS):
            raise Exception("All out of API keys. Try again tomorrow.")
        response = requests.get(url, headers=CoinAPI.HEADERS)
        if response.status_code == 429:
            CoinAPI.API_KEY_IDX = (CoinAPI.API_KEY_IDX + 1) % len(CoinAPI.API_KEYS)
            return CoinAPI.make_request(url, attempt + 1)
        return response.text

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
            for asset in json.loads(f.read()):
                if asset["symbol_id"] == f"{EXCHANGE}_SPOT_{symbol}_USD":
                    return asset["data_start"]

    @staticmethod
    def get_ohlcv(symbol, timeframe, start_date, end_date=None, limit=100) -> str:
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

        return CoinAPI.make_request(url)

    @staticmethod
    def get_assets() -> str:
        return CoinAPI.make_request(f"{URL_BASE}/assets")

    @staticmethod
    def get_symbols() -> str:
        return CoinAPI.make_request(f"{URL_BASE}/symbols")
