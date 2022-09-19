from finance import Utils

import numba as nb
import numpy as np
from scipy import stats


def get_hd_dates(hd):
    return np.arange(hd.start_date, hd.end_date + hd.interval, hd.interval)

def __find_time_delta(dates):
    return stats.mode(dates[1:] - dates[:-1])

@nb.njit(cache=True)
def __create_array(dates, prices, interval, size):
    j = 0; values = np.empty(size)

    for i in range(len(prices) - 1):
        n = round((dates[i + 1] - dates[i]) / interval)
        values[j:j + n] = prices[i]
        j += n

    values[-1] = prices[-1]
    return values


def create_hd_from_series(series, start_date=Utils.MIN_DATETIME, end_date=Utils.MIN_DATETIME,
                          interval=Utils.NO_TIME, label="", scatter=False):
    dates = series.keys().to_numpy(Utils.DATETIME_TYPE)
    prices = series.values

    if start_date != Utils.MIN_DATETIME:
        mask = dates >= start_date
        dates, prices = dates[mask], prices[mask]
    if end_date != Utils.MIN_DATETIME:
        mask = dates <= end_date
        dates, prices = dates[mask], prices[mask]

    start_date, end_date = dates[0], dates[-1]
    if interval == Utils.NO_TIME:
        interval = __find_time_delta(dates)

    size = round((end_date + interval - start_date) / interval)
    values = __create_array(dates, prices, interval, size)

    Utils.write_to_file("file.txt", values)

    return HistoricalData(values=values, interval=interval, start_date=start_date,
                          end_date=end_date, label=label, scatter=scatter)


spec = [
    ("values", nb.float64[:]),
    ("interval", Utils.NB_TIMEDELTA),
    ("start_date", Utils.NB_DATETIME),
    ("end_date", Utils.NB_DATETIME),
    ("label", nb.types.unicode_type),
    ("scatter", nb.boolean)
]


@nb.experimental.jitclass(spec)
class HistoricalData:
    def __init__(self, values, interval=Utils.NO_TIME, start_date=Utils.MIN_DATETIME,
                 end_date=Utils.MIN_DATETIME, label="", scatter=False):
        self.values = values
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date
        self.label = label
        self.scatter = scatter

        self.__init_from_numpy_array()

    def __mul__(self, num: float):
        try:
            float(num)
        except Exception:
            raise Exception("HistoricalData must be multiplied by a number")

        return HistoricalData(self.values * num, self.interval, self.start_date, self.end_date, self.label, self.scatter)

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

    def __init_from_numpy_array(self):
        n = len(self.values)
        num_provided = int(self.interval != Utils.NO_TIME) + \
                       int(self.start_date != Utils.MIN_DATETIME) + \
                       int(self.end_date != Utils.MIN_DATETIME)

        if num_provided < 2:
            raise Exception("Must provide at least 2 of (interval, start_date, or end_date")
        elif num_provided == 2:
            if self.interval == Utils.NO_TIME:
                self.interval = (self.end_date - self.start_date) / (n - 1) if n > 1 else Utils.NO_TIME
            elif self.start_date == Utils.MIN_DATETIME:
                self.start_date = self.end_date - (n - 1) * self.interval
            elif self.end_date == Utils.MIN_DATETIME:
                self.end_date = self.start_date + (n - 1) * self.interval

    def in_bounds(self, date):
        return self.start_date <= date <= self.end_date

    def get_val_by_date(self, date):
        if not self.in_bounds(date):
            raise Exception("Date is out of bounds")
        return self.values[round((date - self.start_date) / self.interval)]
