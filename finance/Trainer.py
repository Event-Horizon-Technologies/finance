from finance.Asset import Asset
from finance.create_asset import create_asset
from finance import Utils

import numpy as np
import os
import pickle
import sys
from keras import activations, callbacks, layers, losses, models, optimizers
from pathlib import Path
from tqdm import tqdm

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'

class Trainer:
    def __init__(self, indicators, prediction_offset=15, validation_split=0.1) -> None:
        self.input_train = self.target_train = self.input_test = self.target_test = None
        self.model = self.indicators = self.prediction_offset = None
        self.input_means = self.target_mean = 0.0
        self.input_stds = self.target_std = 1.0

        self.indicators = indicators
        self.prediction_offset = prediction_offset
        self.validation_split = validation_split

    @property
    def input_size(self) -> int:
        return self.input_train.shape[1] if self.input_train is not None else 0

    def __standardize(self) -> None:
        self.input_means = np.apply_along_axis(np.mean, 0, np.concatenate((self.input_train, self.input_test)))
        self.target_mean = np.mean(np.concatenate((self.target_train, self.target_test)))
        self.input_stds = np.apply_along_axis(np.std, 0, np.concatenate((self.input_train, self.input_test)))
        self.target_std = np.std(np.concatenate((self.target_train, self.target_test)))

        self.input_train = Utils.standardize(self.input_train, self.input_means, self.input_stds)
        self.target_train = Utils.standardize(self.target_train, self.target_mean, self.target_std)
        self.input_test = Utils.standardize(self.input_test, self.input_means, self.input_stds)
        self.target_test = Utils.standardize(self.target_test, self.target_mean, self.target_std)

    @staticmethod
    def __create_assets(symbols, timeframe="1d") -> list[Asset]:
        assets = []
        for symbol in (itr := tqdm(symbols)):
            itr.set_description(f"Downloading data for {symbol}.. ".ljust(40))
            try:
                assets.append(create_asset(symbol=symbol, timeframe=timeframe))
            except ValueError: pass
        return assets

    @staticmethod
    def create_pickled_assets(symbols, timeframe, pickle_path) -> None:
        with open(pickle_path, "wb") as f:
            pickle.dump(Trainer.__create_assets(symbols, timeframe), f)

    def save_model(self, path) -> None:
        self.model.save(path)

    def create_model(self, hidden_layers=8, width=128, activation=activations.selu, dropout=0.5) -> None:
        self.model = models.Sequential()

        self.model.add(layers.Dense(units=width, input_shape=(self.input_size,), activation=activation))
        self.model.add(layers.Dropout(dropout))
        for i in range(hidden_layers):
            self.model.add(layers.Dense(units=width, activation=activation))
            self.model.add(layers.Dropout(dropout))
        self.model.add(layers.Dense(units=1))

        self.model.compile(optimizer=optimizers.SGD(), loss=losses.MeanSquaredError())
        # self.model.compile(optimizer=optimizers.Adam(), loss=losses.MeanSquaredError())

    def generate_indicator_data(self, asset) -> np.ndarray:
        return np.column_stack([i.create_neural_net_data(asset) for i in self.indicators])

    def generate_data(self, saved_assets=None, symbols=None, timeframe="1d") -> None:
        if not (saved_assets or symbols):
            raise Exception("No assets to generate data with. Must provide either 'symbols' or 'saved_assets'")

        if saved_assets:
            with open(Path(saved_assets), "rb") as f:
                assets = pickle.load(f)
        else:
            assets = self.__create_assets(symbols, timeframe)

        input_train = []; target_train = []; input_test = []; target_test = []
        data_points = sum(len(asset.close.values) - self.prediction_offset for asset in assets)
        test_offset = round(self.validation_split * data_points / len(assets))
        test_offset = min(test_offset, min(len(asset.close.values) for asset in assets))

        for asset in assets:
            prices = asset.close.values

            input_data = self.generate_indicator_data(asset)[:-self.prediction_offset]
            target_data = np.log(prices[self.prediction_offset:] / prices[:-self.prediction_offset])

            input_train.append(input_data[:-test_offset])
            target_train.append(target_data[:-test_offset])

            input_test.append(input_data[-test_offset:])
            target_test.append(target_data[-test_offset:])

        self.input_train, self.target_train = np.concatenate(input_train), np.concatenate(target_train)
        self.input_test, self.target_test = np.concatenate(input_test), np.concatenate(target_test)

        self.__standardize()

    def train(self, batch_size=sys.maxsize, epochs=300, patience=3) -> None:
        self.model.fit(x=self.input_train, y=self.target_train, validation_data=(self.input_test, self.target_test),
                       batch_size=batch_size, epochs=epochs, callbacks=callbacks.EarlyStopping(patience=patience))

    def predict(self, input_data, standardized=False) -> np.ndarray:
        if not standardized:
            input_data = Utils.standardize(input_data, self.input_means, self.input_stds)

        if input_data.ndim == 1:
            prediction = self.model.predict(np.expand_dims(input_data, axis=0), verbose=0)[0]
        else:
            prediction = self.model.predict(input_data, verbose=0)

        if not standardized:
            prediction = Utils.unstandardize(prediction, self.target_mean, self.target_std)

        return prediction

    def load_data(self, path_to_data) -> None:
        with open(path_to_data, "rb") as f:
            self.__dict__ = pickle.load(f)

    def save_data(self, path_to_data) -> None:
        with open(path_to_data, "wb") as f:
            pickle.dump(self.__dict__, f)
