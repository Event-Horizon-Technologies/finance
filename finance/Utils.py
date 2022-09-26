import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATETIME_SYMBOL = 'm'
DATETIME_TYPE = f"datetime64[{DATETIME_SYMBOL}]"
PICKLE_GENERATION_MODE = '1'

INTERVALS = {
    "1d": np.timedelta64(1, 'D'),
    "1h": np.timedelta64(1, 'h'),
    "5m": np.timedelta64(5, 'm'),
    "1m": np.timedelta64(1, 'm')
}

MAX = {
    "1d": "max",
    "1h": "730d",
    "5m": "60d",
    "1m": "7d"
}

class Format:
    def __init__(self):
        raise Exception(f"Cannot instantiate static class {self.__class__.__name__}")
    
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NONE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    


def show_plot():
    plt.legend(loc="best", prop={"size": 10})
    plt.show()

def create_np_datetime(timestamp):
    return timestamp.to_datetime64().astype({DATETIME_TYPE})

def create_pd_timestamp(datetime, tz_aware=True):
    return pd.Timestamp(datetime).tz_localize("UTC").tz_convert("UTC") if tz_aware else pd.Timestamp(datetime)

def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(str(data))

def read_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()
