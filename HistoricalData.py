from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np

class HistoricalData:
    def __init__(self, **kwargs):
        dictionary = kwargs.get("dictionary")

        self.array = kwargs.get("array")
        self.interval = kwargs.get("interval")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")

        if dictionary is None and self.array is None:
            raise Exception("Must provide either an array or a dict")

        if dictionary:
            self.__init_from_dict(dictionary)
        else:
            self.__init_from_array()

    def __init_from_dict(self, dictionary):
        if self.interval is None:
            self.interval = self.__find_time_delta(dictionary)
        self.__create_array(dictionary)

    def __init_from_array(self):
        n = len(self.array)
        num_provided = sum([0 if var is None else 1 for var in (self.interval, self.start_date, self.end_date)])

        if num_provided < 2:
            raise Exception("Must provide at least 2 of (interval, start_date, or end_date")
        elif num_provided == 2:
            if self.interval is None:
                self.interval = (self.end_date - self.start_date) / n
            elif self.start_date is None:
                self.start_date = self.end_date - n * self.interval
            elif self.end_date is None:
                self.end_date = self.start_date + n * self.interval

    def __find_time_delta(self, dictionary):
        time_deltas = {}

        delta = last_date_time = None
        for date_time, value in dictionary.items():
            if last_date_time:
                delta = date_time - last_date_time
            if delta in time_deltas:
                time_deltas[delta] += 1
            else:
                time_deltas[delta] = 1
            last_date_time = date_time

        max_delta = timedelta(0)
        max_count = 0
        for delta, count in time_deltas.items():
            if count > max_count:
                max_count = count
                max_delta = delta

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
                values.append(dictionary[today])
                today += self.interval
            else:
                interpolated_values = self.__get_interpolated_values(today, dictionary)
                values += interpolated_values
                today += len(interpolated_values) * self.interval

        self.array = np.array(values, dtype=float)

    def __get_interpolated_values(self, today, dictionary):
        if today >= self.end_date:
            return []

        first = today - self.interval
        last = today

        initial_value = dictionary[first]

        days_skipped = 0
        while last not in dictionary:
            last += self.interval
            days_skipped += 1

        total_mult = dictionary[last] / dictionary[first]
        mult = total_mult ** (1.0 / (days_skipped+1))

        return [initial_value * mult ** i for i in range(1, days_skipped+1)]

    def to_dict(self):
        return {self.start_date + i * self.interval: self.array[i] for i in range(len(self.array))}

    def plot(self, label="Label"):
        dictionary = self.to_dict()
        plt.plot(dictionary.keys(), dictionary.values(), label=label)

