import matplotlib.pyplot as plt

DATETIME_TYPE = 'm'
PICKLE_GENERATION_MODE = '1'

def show_plot():
    plt.legend(loc="best", prop={"size": 10})
    plt.show()

def create_np_datetime(timestamp):
    return timestamp.to_datetime64().astype(f"datetime64[{DATETIME_TYPE}]")
