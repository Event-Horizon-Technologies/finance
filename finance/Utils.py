import numpy as np
import numba as nb
import pandas as pd

from datetime import datetime

DATETIME_SYMBOL = 'm'
DATETIME_TYPE = f"datetime64[{DATETIME_SYMBOL}]"
TIMEDELTA_TYPE = f"timedelta64[{DATETIME_SYMBOL}]"

NO_TIME = np.timedelta64(0, DATETIME_SYMBOL)
MIN_DATETIME = np.datetime64(datetime.min, DATETIME_SYMBOL)

NB_DATETIME = nb.from_dtype(MIN_DATETIME.dtype)
NB_TIMEDELTA = nb.from_dtype(NO_TIME.dtype)

PICKLE_GENERATION_MODE = '1'

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
