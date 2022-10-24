from finance.Static import Static

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATETIME_SYMBOL = 'm'
DATETIME_TYPE = f"datetime64[{DATETIME_SYMBOL}]"
PICKLE_GENERATION_MODE = '1'
MAX = {
    "1d": "max",
    "1h": "730d",
    "5m": "60d",
    "1m": "7d"
}

def convert_interval(timeframe):
    match timeframe:
        case "1d" | "1DAY": return np.timedelta64(1, 'D')
        case "1h" | "1HRS": return np.timedelta64(1, 'h')
        case "5m" | "5MIN": return np.timedelta64(5, 'm')
        case "1m" | "1MIN": return np.timedelta64(1, 'm')
    raise ValueError(f"Cannot create timedelta64 from {timeframe}")

class Format(Static):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NONE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def blue(string) -> str:
        return f"{Format.BLUE}{string}{Format.NONE}"

    @staticmethod
    def green(string) -> str:
        return f"{Format.GREEN}{string}{Format.NONE}"

    @staticmethod
    def yellow(string) -> str:
        return f"{Format.YELLOW}{string}{Format.NONE}"

    @staticmethod
    def red(string) -> str:
        return f"{Format.RED}{string}{Format.NONE}"

    @staticmethod
    def bold(string) -> str:
        return f"{Format.BOLD}{string}{Format.NONE}"

    @staticmethod
    def underline(string) -> str:
        return f"{Format.UNDERLINE}{string}{Format.NONE}"

def show_plot() -> None:
    plt.legend(loc="best", prop={"size": 10})
    plt.show()

def create_np_datetime(timestamp) -> np.datetime64:
    return timestamp.to_datetime64().astype({DATETIME_TYPE})

def create_pd_timestamp(datetime, tz_aware=True) -> pd.Timestamp:
    return pd.Timestamp(datetime).tz_localize("UTC").tz_convert("UTC") if tz_aware else pd.Timestamp(datetime)

def write_to_file(file_name, data) -> None:
    with open(file_name, 'w') as f:
        f.write(str(data))

def read_from_file(file_name) -> None:
    with open(file_name, 'r') as f:
        return f.read()
