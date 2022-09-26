from finance.Asset import Asset

import numpy as np
import pickle
from keras import activations, layers, losses, models, optimizers

class Trainer:
    def __init__(self):
        self.input_data = self.target_data = self.model = None
        self.input_means = self.target_mean = 0.0
        self.input_stds = self.target_std = 1.0

    @property
    def input_size(self):
        return self.input_data.shape[1] if self.input_data is not None else 0

    def __standardize(self):
        self.input_means = np.apply_along_axis(np.mean, 0, self.input_data)
        self.target_mean = np.mean(self.target_data)

        self.input_data -= self.input_means
        self.target_data -= self.target_mean

        self.input_stds = np.apply_along_axis(np.std, 0, self.input_data)
        self.target_std = np.std(self.target_data)

        self.input_data /= self.input_stds
        self.target_data /= self.target_std

    def create_model(self, hidden_layers=8, width=16, activation=activations.selu, dropout=0.5):
        self.model = models.Sequential()

        self.model.add(layers.Dense(units=width, input_shape=(self.input_size,), activation=activation))
        self.model.add(layers.Dropout(dropout))
        for i in range(hidden_layers):
            self.model.add(layers.Dense(units=width, activation=activation))
            self.model.add(layers.Dropout(dropout))
        self.model.add(layers.Dense(units=1))

        self.model.compile(optimizer=optimizers.SGD(), loss=losses.MeanSquaredError())

    def generate_data(self, symbols, indicators, timeframe="1d", prediction_offset=30):
        input_data = []; target_data = []

        for symbol in symbols:
            asset = Asset(symbol=symbol, timeframe=timeframe)
            prices = asset.close.values

            input_data.append(np.column_stack([i.create_neural_net_data(asset, prediction_offset) for i in indicators]))
            target_data.append(np.log(prices[prediction_offset:] / prices[:-prediction_offset]))

        self.input_data, self.target_data = np.concatenate(input_data), np.concatenate(target_data)
        self.__standardize()

    def train(self, batch_size=32, epochs=100):
        self.model.fit(x=self.input_data, y=self.target_data, batch_size=batch_size, epochs=epochs)

    def load_data(self, path_to_data):
        with open(path_to_data, "rb") as f:
            self.__dict__ = pickle.load(f)

    def save_data(self, path_to_data):
        with open(path_to_data.joinpath("input_data.pickle"), "wb") as f:
            pickle.dump(self.__dict__, f)
