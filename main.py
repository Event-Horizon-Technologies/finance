#!/usr/bin/python
from finance import Asset, Indicators, Simulator, Strategy, Trainer, Utils

import numpy as np
import sys
from pathlib import Path

DATA_PATH = Path(__file__).parent.joinpath("data")
CRYPTOS_FILE = DATA_PATH.joinpath("cryptos.txt")
PICKLE_FILE = DATA_PATH.joinpath("trainer.pickle")

def get_symbols():
    with open(CRYPTOS_FILE) as f:
        return [symbol.strip() for symbol in f.readlines()]

def main(argv):
    symbol    = argv[0] if len(argv) > 0 else "BTC-USD"
    timeframe = argv[1] if len(argv) > 1 else "1d"

    symbols = get_symbols()
    indicators = [Indicators.PSAR(), Indicators.EMA(20), Indicators.EMA(40)]

    trainer = Trainer()
    # trainer.generate_data(symbols, indicators, timeframe="1m")
    # trainer.save_data(PICKLE_FILE)
    trainer.load_data(PICKLE_FILE)
    trainer.create_model()
    trainer.train()  # https://www.youtube.com/watch?v=5dx3XD46fE0


if __name__ == "__main__":
    main(sys.argv[1:])
