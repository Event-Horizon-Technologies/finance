import Utils

import matplotlib.pyplot as plt
import numpy as np
import numba as nb
from scipy import stats


class HistoricalData:
    def __init__(self, **kwargs):
        dictionary = kwargs.get("dictionary")

        self.values = kwargs.get("values")
        self.interval = kwargs.get("interval")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.label = kwargs.get("label")
        self.scatter = kwargs.get("scatter")

        if dictionary is None and self.values is None:
            raise Exception("Must provide either an array or a dict")

        if dictionary:
            self.__init_from_dict(dictionary)
        else:
            self.__init_from_array()

    def __mul__(self, num):
        try:
            float(num)
        except TypeError:
            raise Exception("HistoricalData must be multiplied by a number")

        return HistoricalData(values=self.values * num, start_date=self.start_date, end_date=self.end_date)

    def __init_from_dict(self, dictionary):
        dates = np.fromiter(sorted(dictionary.keys()), 'datetime64[s]')
        prices = np.fromiter((dictionary[date] for date in dates), float)
        self.start_date, self.end_date = dates[0], dates[-1]
        if self.interval is None:
            self.interval = self.__find_time_delta(dates)

        size = round((self.end_date + self.interval - self.start_date) / self.interval)
        self.values = self.__create_array(dates, prices, self.interval, size)

    def __init_from_array(self):
        n = len(self.values)
        num_provided = sum([var is not None for var in (self.interval, self.start_date, self.end_date)])

        if num_provided < 2:
            raise Exception("Must provide at least 2 of (interval, start_date, or end_date")
        elif num_provided == 2:
            if self.interval is None:
                self.interval = (self.end_date - self.start_date) / (n - 1) if n > 1 else np.timedelta64(0)
            elif self.start_date is None:
                self.start_date = self.end_date - (n - 1) * self.interval
            elif self.end_date is None:
                self.end_date = self.start_date + (n - 1) * self.interval

    @staticmethod
    def __find_time_delta(dates):
        return stats.mode(dates[1:] - dates[:-1])

    @staticmethod
    @nb.njit()
    def __create_array(dates, prices, interval, size):
        i = j = 0; date = dates[0]; values = np.empty(size)

        while i < len(prices) - 1:
            price = prices[i]
            while date < dates[i+1]:
                values[j] = price
                date += interval
                j += 1
            i += 1

        values[-1] = prices[-1]
        return values

    def in_bounds(self, date):
        return self.start_date <= date <= self.end_date

    def get_val_by_date(self, date):
        if not self.in_bounds(date):
            raise Exception(f"Date {date} is out of bounds")
        return self.values[round((date - self.start_date) / self.interval)]

    def to_dict(self):
        return {self.start_date + i * self.interval: self.values[i] for i in range(len(self.values))}

    def plot(self, label=None, show=True):
        if label is None: label = self.label
        dictionary = self.to_dict()
        if self.scatter:
            plt.scatter(dictionary.keys(), dictionary.values(), label=label, s=2, c="orange")
        else:
            plt.plot(dictionary.keys(), dictionary.values(), label=label)
        if show:
            Utils.show_plot()
