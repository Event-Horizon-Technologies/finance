from finance.Static import Static

import pandas
import requests
from io import StringIO
from pathlib import Path

URL_BASE = "https://www.alphavantage.co/query?"
SYMBOL = "TSLA"
INTERVAL = "5min"
API_KEY = "ZZ7E9KFFYTKGZ0XR"
CRYPTO_LIST = Path(__file__).parent.joinpath("crypto_list.txt")

"""finance AlphaVantageAPI wrapper class"""
class AlphaVantage(Static):
    def __init__(self):
        super().__init__()
    
    """Core Stock API start"""
    @staticmethod
    def get_intraday_request(symbol, interval, adjusted="true", outputsize="compact", datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={API_KEY}"
        )
    
    @staticmethod
    def get_intraday_extended_request(symbol, interval, slice="year1month1", adjusted="true"):
        return requests.get(
            f"{URL_BASE}function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval={interval}&slice={slice}&adjusted={adjusted}&apikey={API_KEY}"
        )

    @staticmethod
    def get_daily_request(symbol, outputsize="compact", datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&datatype={datatype}&apikey={API_KEY}"
        )

    @staticmethod
    def get_daily_adjusted_request(symbol, outputsize="compact", datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=TIME_SERIES_DALY_ADJUSTED&symbol={symbol}&outputsize={outputsize}&datatype={datatype}&apikey={API_KEY}"
        )

    @staticmethod
    def get_weekly_request(symbol, datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=TIME_SERIES_WEEKLY&symbol={symbol}&datatype={datatype}&apikey={API_KEY}"
        )

    @staticmethod
    def get_monthly_request(symbol, datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=TIME_SERIES_MONTHLY&symbol={symbol}&datatype={datatype}&apikey={API_KEY}"
        )

    @staticmethod
    def get_monthly_adjusted_request(symbol, datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&datatype={datatype}&apikey={API_KEY}"
        )

    @staticmethod
    def get_quote_endpoint_request(symbol, datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=GLOBAL_QUOTE&symbol={symbol}&datatype={datatype}&apikey={API_KEY}"
        )
    
    @staticmethod
    def get_search_endpoint_request(keywords, datatype="csv"):
        return requests.get(
            f"{URL_BASE}function=SYMBOL_SEARCH&keywords={keywords}&datatype={datatype}&apikey={API_KEY}"
        )
    """Core Stock API end"""

    """Alpha Intelligence start"""
    @staticmethod
    def get_news_and_sentiments(tickers="", topics="", time_from="", time_to="", sort="LATEST", limit="50"):
        return requests.get(
            f"{URL_BASE}function=NEWS_SENTIMENT&tickers={tickers}&topics={topics}&time_from={time_from}&time_to={time_to}&sort={sort}&limit={limit}&apikey={API_KEY}"
        )
    
    @staticmethod
    def get_winning_portfolios(season):
        return requests.get(
            f"{URL_BASE}function=TOURNAMENT_PORTFOLIO&season={season}&apikey={API_KEY}"
        )
    """Alpha Intelligence end"""

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
