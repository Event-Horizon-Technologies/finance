from finance.Asset import Asset

import numpy as np
import pickle
import tensorflow as tf
from tensorflow import keras

class Trainer:
    def __init__(self):
        self.input_data = self.target_data = None

    @property
    def input_size(self):
        return self.input_data.shape[1] if self.input_data else 0

    def create_model(self, hidden_layers=8, width=16, activation=keras.activations.selu, dropout=0.5):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(units=width, input_shape=(self.input_size,), activation=activation))
        model.add(keras.layers.Dropout(dropout))
        for i in range(hidden_layers):
            model.add(keras.layers.Dense(units=width, activation=activation))
            model.add(keras.layers.Dropout(dropout))
        model.add(keras.layers.Dense(units=1))
        return model

    def generate_data(self, symbols, indicators, timeframe="1d", prediction_offset=30):
        input_data = []; target_data = []

        for symbol in symbols:
            asset = Asset(symbol=symbol, timeframe=timeframe)
            prices = asset.close.values

            input_data.append(np.column_stack([i.create_neural_net_data(asset, prediction_offset) for i in indicators]))
            target_data.append(np.log(prices[prediction_offset:] / prices[:-prediction_offset]))

        self.input_data, self.target_data = np.concatenate(input_data), np.concatenate(target_data)

    def load_data(self, path_to_data):
        with open(path_to_data.joinpath("input_data.pickle"), "rb") as f:
            self.input_data = pickle.load(f)
        with open(path_to_data.joinpath("target_data.pickle"), "rb") as f:
            self.target_data = pickle.load(f)

    def save_data(self, path_to_data):
        with open(path_to_data.joinpath("input_data.pickle"), "wb") as f:
            pickle.dump(self.input_data, f)
        with open(path_to_data.joinpath("target_data.pickle"), "wb") as f:
            pickle.dump(self.target_data, f)
