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
OUTPUTSIZE = "full"
ADJUSTED = "true"
MARKET = "USD"

def is_crypto(symbol):
    with open(CRYPTO_LIST) as f:
        for line in f.readlines():
            if symbol == line.strip():
                return True
    return False

def get_pandas_dataframe(url, include_metadata=True):
    url += f"&datatype={'json' if include_metadata else 'csv'}"
    response = requests.get(url).content.decode("UTF-8")
    func = pandas.read_json if include_metadata else pandas.read_csv
    return func(StringIO(response))


class AlphaVantage(Static):
    """finance AlphaVantageAPI wrapper class"""
    
    """Core Stock API start"""
    @staticmethod
    def get_intraday_stock_data(symbol, interval, adjusted=ADJUSTED, outputsize=OUTPUTSIZE, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}",
            include_metadata=include_metadata
        )
    
    @staticmethod
    def get_intraday_extended_stock_data(symbol, interval, slice="year1month1", adjusted=ADJUSTED, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval={interval}&slice={slice}&adjusted={adjusted}&apikey={API_KEY}",
            include_metadata=include_metadata
        )

    @staticmethod
    def get_daily_stock_data(symbol, outputsize=OUTPUTSIZE, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&apikey={API_KEY}",
            include_metadata=include_metadata
        )

    @staticmethod
    def get_daily_adjusted_stock_data(symbol, outputsize=OUTPUTSIZE, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TIME_SERIES_DALY_ADJUSTED&symbol={symbol}&outputsize={outputsize}&apikey={API_KEY}",
            include_metadata=include_metadata
        )

    @staticmethod
    def get_weekly_stock_data(symbol, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={API_KEY}",
            include_metadata=include_metadata
        )

    @staticmethod
    def get_monthly_stock_data(symbol, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={API_KEY}",
            include_metadata=include_metadata
        )

    @staticmethod
    def get_monthly_adjusted_stock_data(symbol, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}",
            include_metadata=include_metadata
        )

    @staticmethod
    def get_quote_endpoint_data(symbol, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}",
            include_metadata=include_metadata
        )
    
    @staticmethod
    def get_search_endpoint_data(keywords, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=SYMBOL_SEARCH&keywords={keywords}&apikey={API_KEY}",
            include_metadata=include_metadata
        )
    """Core Stock API end"""

    """Alpha Intelligence start"""
    @staticmethod
    def get_news_and_sentiments_data(tickers="", topics="", time_from="", time_to="", sort="LATEST", limit="50", include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=NEWS_SENTIMENT&tickers={tickers}&topics={topics}&time_from={time_from}&time_to={time_to}&sort={sort}&limit={limit}&apikey={API_KEY}",
            include_metadata=include_metadata
        )
    
    @staticmethod
    def get_winning_portfolios_data(season, include_metadata=True):
        return get_pandas_dataframe(
            f"{URL_BASE}function=TOURNAMENT_PORTFOLIO&season={season}&apikey={API_KEY}",
            include_metadata=include_metadata
        )
    """Alpha Intelligence end"""

    @staticmethod
    def get_stock_data(symbol, interval, include_metadata=True, outputsize=OUTPUTSIZE):
        function = "TIME_SERIES_DAILY" if interval == "1day" else "TIME_SERIES_INTRADAY_EXTENDED"
        url = f"{URL_BASE}function={function}&symbol={symbol}&apikey={API_KEY}&outputsize={outputsize}"
        if interval != "1day": url += f"&interval={interval}"
        return get_pandas_dataframe(url, include_metadata=include_metadata)

    @staticmethod
    def get_crypto_data(symbol, interval, include_metadata=True, market=MARKET):
        function = "DIGITAL_CURRENCY_DAILY" if interval == "1day" else "CRYPTO_INTRADAY"
        url = f"{URL_BASE}function={function}&symbol={symbol}&apikey={API_KEY}&market={market}"
        if interval != "1day": url += f"&interval={interval}"
        return get_pandas_dataframe(url, include_metadata=include_metadata)
