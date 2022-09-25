import numpy as np

from finance.Asset import Asset
from finance import Utils

import tensorflow as tf
from tensorflow import keras

class Trainer:
    def __init__(self):
        pass

    @staticmethod
    def generate_data(symbols, indicators, timeframe="1d", prediction_offset=30):
        input_data = []; target_data = []

        for symbol in symbols:
            asset = Asset(symbol=symbol, timeframe=timeframe)
            prices = asset.close.values

            input_data.append(np.column_stack([i.create_neural_net_data(asset, prediction_offset) for i in indicators]))
            target_data.append(np.log(prices[prediction_offset:] / prices[:-prediction_offset]))

        return np.concatenate(input_data), np.concatenate(target_data)



