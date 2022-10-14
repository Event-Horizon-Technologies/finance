from finance.Static import Static

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

DATETIME_SYMBOL = 'm'
DATETIME_TYPE = f"datetime64[{DATETIME_SYMBOL}]"
PICKLE_GENERATION_MODE = '1'
CRYPTO_LIST = Path(__file__).parent.joinpath("crypto_list.txt")

INTERVALS = {
    "1day" : np.timedelta64(1, 'D'),
    "60min": np.timedelta64(1, 'h'),
    "5min" : np.timedelta64(5, 'm'),
    "1min" : np.timedelta64(1, 'm')
}

MAX = {
    "1d": "max",
    "1h": "730d",
    "5m": "60d",
    "1m": "7d"
}

class Format(Static):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NONE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        super().__init__()

    @staticmethod
    def blue(string):
        return f"{Format.BLUE}{string}{Format.NONE}"

    @staticmethod
    def green(string):
        return f"{Format.GREEN}{string}{Format.NONE}"

    @staticmethod
    def yellow(string):
        return f"{Format.YELLOW}{string}{Format.NONE}"

    @staticmethod
    def red(string):
        return f"{Format.RED}{string}{Format.NONE}"

    @staticmethod
    def bold(string):
        return f"{Format.BOLD}{string}{Format.NONE}"

    @staticmethod
    def underline(string):
        return f"{Format.UNDERLINE}{string}{Format.NONE}"

def show_plot():
    plt.legend(loc="best", prop={"size": 10})
    plt.show()

def create_np_datetime(timestamp):
    if isinstance(timestamp, str):
        return np.datetime64(timestamp).astype(DATETIME_TYPE)
    return timestamp.to_datetime64().astype(DATETIME_TYPE)

def create_pd_timestamp(datetime, tz_aware=True):
    return pd.Timestamp(datetime).tz_localize("UTC").tz_convert("UTC") if tz_aware else pd.Timestamp(datetime)

def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(str(data))

def read_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def is_crypto(symbol):
    with open(CRYPTO_LIST) as f:
        for line in f.readlines():
            if symbol == line.strip():
                return True
    return False