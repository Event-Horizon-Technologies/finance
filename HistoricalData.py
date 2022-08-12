from datetime import datetime, timedelta, timezone
import numpy as np

class HistoricalData:
    def __init__(self, dictionary, interval=None):
        self.interval = interval if interval else self.__find_time_delta(dictionary)

        self.__create_array(dictionary, self.interval)

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

    def __create_array(self, dictionary, interval):
        dates = list(dictionary.keys())
        dates.sort()

        self.start_date = dates[0]
        self.end_date = dates[-1]
        self.interval = interval

        values = []
        today = self.start_date
        while today <= self.end_date:
            if today in dictionary:
                values.append(dictionary[today])
            else:
                interpolated_values = self.__get_interpolated_values(today, dictionary)
                values += interpolated_values
                today += len(interpolated_values) * interval
            today += interval

        self.values = np.array(values, dtype=float)

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
        return {self.start_date + i * self.interval: self.values[i] for i in range(len(self.values))}
