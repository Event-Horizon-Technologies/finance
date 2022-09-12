import matplotlib.pyplot as plt
import pandas as pd

DATETIME_TYPE = 'm'
PICKLE_GENERATION_MODE = '1'

def show_plot():
    plt.legend(loc="best", prop={"size": 10})
    plt.show()

def create_np_datetime(timestamp):
    return timestamp.to_datetime64().astype(f"datetime64[{DATETIME_TYPE}]")

def create_pd_timestamp(datetime, tz_aware=True):
    return pd.Timestamp(datetime).tz_localize("UTC").tz_convert("UTC") if tz_aware else pd.Timestamp(datetime)

def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(str(data))

def read_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()
