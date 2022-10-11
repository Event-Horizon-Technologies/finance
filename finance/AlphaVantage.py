import Utils

import pandas
import requests
from io import StringIO
from pathlib import Path

URL_BASE = "https://www.alphavantage.co/query?"
SYMBOL = "TSLA"
INTERVAL = "5min"
API_KEY = "ZZ7E9KFFYTKGZ0XR"
CRYPTO_LIST = Path(__file__).parent.joinpath("crypto_list.txt")

class AlphaVantage(Utils.Static):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_intraday_url(symbol, interval, adjusted="true", outputsize="compact", datatype="csv"):
        return f"{URL_BASE}function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={API_KEY}"
    
    @staticmethod
    def get_intraday_extended_url(symbol, interval, slice="year1month1", adjusted="true"):
        return f"{URL_BASE}function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval={interval}&slice={slice}&adjusted={adjusted}&apikey={API_KEY}"

def is_crypto(symbol):
    with open(CRYPTO_LIST) as f:
        for line in f.readlines():
            if symbol == line.strip():
                return True
    return False

def get_function(symbol, interval):
    if is_crypto(symbol):
        return "DIGITAL_CURRENCY_DAILY" if interval == "1day" else "CRYPTO_INTRADAY"
    return "TIME_SERIES_DAILY" if interval == "1day" else "TIME_SERIES_INTRADAY_EXTENDED"


def call(symbol, interval):
    url = f"{URL_BASE}symbol={symbol}&apikey={API_KEY}&datatype=csv"
    if is_crypto(symbol):
        url += f"&function={'DIGITAL_CURRENCY_DAILY' if interval == '1day' else 'CRYPTO_INTRADAY'}&market=USD" 
    else:
        url += f"&function={'TIME_SERIES_DAILY' if interval == '1day' else 'TIME_SERIES_INTRADAY_EXTENDED'}&outputsize=full"
        
    if interval != "1day":
        url += f"&interval={interval}"

    return requests.get(url)


response = call(SYMBOL, INTERVAL).content.decode("UTF-8")
print(pandas.read_csv(StringIO(response)))
