from finance.Asset import Asset

from keras import activations, callbacks, layers, losses, models, optimizers
import numpy as np
import pickle
import sys

class Trainer:
    def __init__(self):
        self.input_train = self.target_train = self.input_test = self.target_test = self.model = None
        self.input_means = self.target_mean = 0.0
        self.input_stds = self.target_std = 1.0

    @property
    def input_size(self):
        return self.input_train.shape[1] if self.input_train is not None else 0

    def __standardize(self):
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

    def create_model(self, hidden_layers=8, width=16, activation=activations.selu, dropout=0.5):
        self.model = models.Sequential()

        self.model.add(layers.Dense(units=width, input_shape=(self.input_size,), activation=activation))
        self.model.add(layers.Dropout(dropout))
        for i in range(hidden_layers):
            self.model.add(layers.Dense(units=width, activation=activation))
            self.model.add(layers.Dropout(dropout))
        self.model.add(layers.Dense(units=1))

        self.model.compile(optimizer=optimizers.SGD(), loss=losses.MeanSquaredError())

    def generate_data(self, symbols, indicators, timeframe="1d", prediction_offset=30, validation_split=0.1):
        input_train = []; target_train = []; input_test = []; target_test = []
        assets = [Asset(symbol=symbol, timeframe=timeframe) for symbol in symbols]
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

    def train(self, batch_size=sys.maxsize, epochs=sys.maxsize, patience=3):
        self.model.fit(x=self.input_train, y=self.target_train, validation_data=(self.input_test, self.target_test),
                       batch_size=batch_size, epochs=epochs, callbacks=callbacks.EarlyStopping(patience=patience))

    def load_data(self, path_to_data):
        with open(path_to_data, "rb") as f:
            self.__dict__ = pickle.load(f)

    def save_data(self, path_to_data):
        with open(path_to_data, "wb") as f:
            pickle.dump(self.__dict__, f)
