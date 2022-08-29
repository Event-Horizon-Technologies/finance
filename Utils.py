import matplotlib.pyplot as plt

def show_plot():
    plt.legend(loc='best', prop={'size': 10})
    plt.show()
    
def create_np_datetime(timestamp):
    return timestamp.to_datetime64().astype('datetime64[s]')
