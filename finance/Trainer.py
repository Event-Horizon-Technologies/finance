import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

from finance.Asset import Asset

import numpy as np
import pickle
import sys
from keras import activations, callbacks, layers, losses, models, optimizers
from pathlib import Path

class Trainer:
    def __init__(self) -> None:
        self.input_train = self.target_train = self.input_test = self.target_test = self.model = None
        self.input_means = self.target_mean = 0.0
        self.input_stds = self.target_std = 1.0

    @property
    def input_size(self) -> int:
        return self.input_train.shape[1] if self.input_train is not None else 0

    def __standardize(self) -> None:
        self.input_means = np.apply_along_axis(np.mean, 0, np.concatenate((self.input_train, self.input_test)))
        self.target_mean = np.mean(np.concatenate((self.target_train, self.target_test)))

        self.input_stds = np.apply_along_axis(np.std, 0, np.concatenate((self.input_train, self.input_test)))
        self.target_std = np.std(np.concatenate((self.target_train, self.target_test)))

        self.input_train -= self.input_means
        self.target_train -= self.target_mean
        self.input_test -= self.input_means
        self.target_test -= self.target_mean

        self.input_train /= self.input_stds
        self.target_train /= self.target_std
        self.input_test /= self.input_stds
        self.target_test /= self.target_std

    @staticmethod
    def __create_assets(symbols, timeframe="1d") -> list[Asset]:
        return [Asset(symbol=symbol, timeframe=timeframe) for symbol in symbols]

    @staticmethod
    def create_pickled_assets(symbols, timeframe, pickle_path) -> None:
        with open(pickle_path, "wb") as f:
            pickle.dump(Trainer.__create_assets(symbols, timeframe), f)

    def save_model(self, path) -> None:
        self.model.save(path)

    def create_model(self, hidden_layers=16, width=32, activation=activations.selu, dropout=0.5) -> None:
        self.model = models.Sequential()

        self.model.add(layers.Dense(units=width, input_shape=(self.input_size,), activation=activation))
        self.model.add(layers.Dropout(dropout))
        for i in range(hidden_layers):
            self.model.add(layers.Dense(units=width, activation=activation))
            self.model.add(layers.Dropout(dropout))
        self.model.add(layers.Dense(units=1))

        # self.model.compile(optimizer=optimizers.SGD(), loss=losses.MeanSquaredError())
        self.model.compile(optimizer=optimizers.Adam(), loss=losses.MeanSquaredError())

    def generate_data(self, saved_assets=None, symbols=None, timeframe="1d",
                      indicators=None, prediction_offset=30, validation_split=0.1) -> None:
        if not (saved_assets or symbols):
            raise Exception("No assets to generate data with. Must provide either 'symbols' or 'saved_assets'")
        if not indicators:
            raise Exception("No indicators provided")

        if saved_assets:
            with open(Path(saved_assets), "rb") as f:
                assets = pickle.load(f)
        else:
            assets = self.__create_assets(symbols, timeframe)

        input_train = []; target_train = []; input_test = []; target_test = []
        data_points = sum(len(asset.close.values) - prediction_offset for asset in assets)
        test_offset = round(validation_split * data_points / len(assets))
        test_offset = min(test_offset, min(len(asset.close.values) for asset in assets))

        for asset in assets:
            prices = asset.close.values

            input_data = np.column_stack([i.create_neural_net_data(asset, prediction_offset) for i in indicators])
            target_data = np.log(prices[prediction_offset:] / prices[:-prediction_offset])

            input_train.append(input_data[:-test_offset])
            target_train.append(target_data[:-test_offset])

            input_test.append(input_data[-test_offset:])
            target_test.append(target_data[-test_offset:])

        self.input_train, self.target_train = np.concatenate(input_train), np.concatenate(target_train)
        self.input_test, self.target_test = np.concatenate(input_test), np.concatenate(target_test)

        self.__standardize()

    def train(self, batch_size=sys.maxsize, epochs=sys.maxsize, patience=3) -> None:
        self.model.fit(x=self.input_train, y=self.target_train, validation_data=(self.input_test, self.target_test),
                       batch_size=batch_size, epochs=epochs, callbacks=callbacks.EarlyStopping(patience=patience))

    def load_data(self, path_to_data) -> None:
        with open(path_to_data, "rb") as f:
            self.__dict__ = pickle.load(f)

    def save_data(self, path_to_data) -> None:
        with open(path_to_data, "wb") as f:
            pickle.dump(self.__dict__, f)
