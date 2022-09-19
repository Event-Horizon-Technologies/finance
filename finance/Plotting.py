from finance.HistoricalData import HistoricalData, get_hd_dates
from finance.Asset import Asset
from finance.Investment import Investment
from finance.Simulator import Simulator

import matplotlib.pyplot as plt

def show_plot():
    plt.legend(loc="best", prop={"size": 15})
    plt.show()

def __plot_hd(hd, label=""):
    if label == "": label = hd.label
    dates = get_hd_dates(hd)
    if hd.scatter:
        plt.scatter(dates, hd.values, label=label, s=2, c="orange")
    else:
        plt.plot(dates, hd.values, label=label)

def __plot_asset(asset, label="", shares=1.0):
    if label == "": label = asset.symbol
    __plot_hd(asset.close * shares, label)

def __plot_investment(investment, label=""):
    if label == "": label = investment.asset.symbol
    __plot_asset(investment.asset, label, investment.quantity)

def __plot_simulator(simulator, plot_assets=False, plot_indicators=False):
    plt.plot(simulator.strat_hist.keys(), simulator.strat_hist.values(), label=simulator.strategy.label)

    for symbol, investment in simulator.investments.items():
        if plot_assets:
            plot(investment, show=False)

        if plot_indicators:
            for label, hd in simulator.indicator_data[symbol].items():
                plot(hd * investment.quantity, label=f"{symbol} {label}", show=False)

def plot(data, label="", shares=1.0, plot_assets=False, plot_indicators=False, show=True):
    match data:
        case HistoricalData():
            __plot_hd(data, label)
        case Asset():
            __plot_asset(data, label, shares)
        case Investment():
            __plot_investment(data, label)
        case Simulator():
            __plot_simulator(data, plot_assets, plot_indicators)

    if show: show_plot()
