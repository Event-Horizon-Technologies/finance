from finance.AlphaVantage import AlphaVantage
from finance.Asset import Asset

class Crypto(Asset):
    def __init__(self, symbol, interval):
