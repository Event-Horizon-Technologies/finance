from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
from Utils import *

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

        return HistoricalData(values=self.values*num, start_date=self.start_date, end_date=self.end_date)

    def __init_from_dict(self, dictionary):
        if self.interval is None:
            self.interval = self.__find_time_delta(dictionary)
        self.__create_array(dictionary)

    def __init_from_array(self):
        n = len(self.values)
        num_provided = sum([var is not None for var in (self.interval, self.start_date, self.end_date)])

        if num_provided < 2:
            raise Exception("Must provide at least 2 of (interval, start_date, or end_date")
        elif num_provided == 2:
            if self.interval is None:
                self.interval = (self.end_date - self.start_date) / (n - 1) if n > 1 else timedelta(0)
            elif self.start_date is None:
                self.start_date = self.end_date - (n - 1) * self.interval
            elif self.end_date is None:
                self.end_date = self.start_date + (n - 1) * self.interval

    def __find_time_delta(self, dictionary):
        time_deltas = {}

        last_date_time = None
        for date_time in dictionary.keys():
            delta = date_time - last_date_time if last_date_time else None
            time_deltas[delta] = time_deltas[delta] + 1 if delta in time_deltas else 1
            last_date_time = date_time

        max_delta, max_count = timedelta(0), 0
        for delta, count in time_deltas.items():
            if count > max_count:
                max_delta, max_count = delta, count

        return max_delta

    def __create_array(self, dictionary):
        dates = list(dictionary.keys())
        dates.sort()

        self.start_date = dates[0]
        self.end_date = dates[-1]

        values = []
        today = self.start_date
        while today <= self.end_date:
            if today in dictionary:
                values += [dictionary[today]]
                today += self.interval
            else:
                interpolated_values = self.__get_interpolated_values(today, dictionary)
                values += interpolated_values
                today += len(interpolated_values) * self.interval

        self.values = np.array(values)

    def __get_interpolated_values(self, today, dictionary):
        first = today - self.interval
        last = today

        initial_value = dictionary[first]

        days_skipped = 0
        while last not in dictionary:
            last += self.interval
            days_skipped += 1

        final_value = dictionary[last]

        mult = (final_value / initial_value) ** (1.0 / (days_skipped+1))
        # return [initial_value * mult ** i for i in range(1, days_skipped+1)]
        return [initial_value for i in range(1, days_skipped+1)]

    def in_bounds(self, date):
        return date >= self.start_date and date <= self.end_date

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
            show_plot()
