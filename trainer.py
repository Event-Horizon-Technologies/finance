#!/usr/bin/env python3
from finance import Asset, Indicators, Simulator, Strategy, Trainer, Utils

import numpy as np
import sys
from pathlib import Path

DATA_PATH = Path(__file__).parent.joinpath("data")
CRYPTOS_FILE = DATA_PATH.joinpath("top_30_cryptos.txt")
TRAINER_PICKLE = DATA_PATH.joinpath("trainer.pickle")
ASSETS_PICKLE = DATA_PATH.joinpath("assets.pickle")

def get_symbols():
    with open(CRYPTOS_FILE) as f:
        return [symbol.strip() for symbol in f.readlines()]

def main(argv):
    symbol    = argv[0] if len(argv) > 0 else "BTC-USD"
    timeframe = argv[1] if len(argv) > 1 else "1d"

    symbols = get_symbols()
    indicators = [Indicators.PSAR(), Indicators.EMA(2), Indicators.EMA(20), Indicators.EMA(40), Indicators.EMA(200)]

    # Trainer.create_pickled_assets(symbols, "1m", ASSETS_PICKLE)

    trainer = Trainer()
    trainer.generate_data(saved_assets=ASSETS_PICKLE, indicators=indicators)
    # trainer.save_data(TRAINER_PICKLE)
    # trainer.load_data(TRAINER_PICKLE)
    trainer.create_model()
    trainer.train()  # https://www.youtube.com/watch?v=5dx3XD46fE0


if __name__ == "__main__":
    main(sys.argv[1:])
