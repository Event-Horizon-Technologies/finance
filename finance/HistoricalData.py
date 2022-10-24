from datetime import timedelta
from sqlite3 import Timestamp
from finance import Utils

import matplotlib.pyplot as plt
import numba as nb
import numpy as np
from scipy import stats

class HistoricalData:
    def __init__(self, series=None, values=None, interval=None,
                 start_date=None, end_date=None, label=None, scatter=None) -> None:
        self.values = values
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date
        self.label = label
        self.scatter = scatter

        if series is None and self.values is None:
            raise Exception("Must provide either a numpy array or pandas series")

        if series is None:
            self.__init_from_numpy_array()
        else:
            self.__init_from_pandas_series(series)

    def __mul__(self, num):
        try:
            float(num)
        except (TypeError, ValueError):
            raise Exception("HistoricalData must be multiplied by a number")

        return HistoricalData(values=self.values * num, start_date=self.start_date, end_date=self.end_date)
    
    def __eq__(self, other):
        if type(self) != type(other):
            raise TypeError(f"Cannot compare {type(self)} with {type(other)}")

        return (
            np.array_equal(self.values, other.values) and
            self.interval == other.interval and
            self.start_date == other.start_date and
            self.end_date == other.end_date and
            self.label == other.label and
            self.scatter == other.scatter
        )

    def __init_from_pandas_series(self, series) -> None:
        dates = series.keys().to_numpy(Utils.DATETIME_TYPE)
        prices = series.values

        if self.start_date:
            mask = dates >= self.start_date
            dates, prices = dates[mask], prices[mask]
        if self.end_date:
            mask = dates <= self.end_date
            dates, prices = dates[mask], prices[mask]

        self.start_date, self.end_date = dates[0], dates[-1]
        if self.interval is None:
            self.interval = self.__find_time_delta(dates)

        size = round((self.end_date + self.interval - self.start_date) / self.interval)
        self.values = self.__create_array(dates, prices, self.interval, size)

    def __init_from_numpy_array(self) -> None:
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
                
    def create_pd_timestamp(self, datetime) -> Timestamp:
        return Utils.create_pd_timestamp(datetime, tz_aware=(self.interval < np.timedelta64(1, 'D')))

    @staticmethod
    def __find_time_delta(dates) -> timedelta:
        return stats.mode(dates[1:] - dates[:-1])

    @staticmethod
    @nb.njit(cache=True)
    def __create_array(dates, prices, interval, size) -> np.ndarray:
        j = 0; values = np.empty(size)

        for i in range(len(prices) - 1):
            n = round((dates[i+1] - dates[i]) / interval)
            values[j:j+n] = prices[i]
            j += n

        values[-1] = prices[-1]
        return values

    def in_bounds(self, date) -> bool:
        return self.start_date <= date <= self.end_date

    def get_val_by_date(self, date) -> np.ndarray:
        if not self.in_bounds(date):
            raise Exception(f"Date {date} is out of bounds")
        return self.values[round((date - self.start_date) / self.interval)]

    def __get_dates(self) -> np.ndarray:
        return np.arange(self.start_date, self.end_date + self.interval, self.interval)

    def plot(self, label=None, show=True) -> None:
        if label is None: label = self.label
        if self.scatter:
            plt.scatter(self.__get_dates(), self.values, label=label, s=2, c="orange")
        else:
            plt.plot(self.__get_dates(), self.values, label=label)
        if show:
            Utils.show_plot()
