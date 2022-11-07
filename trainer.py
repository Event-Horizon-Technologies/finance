#!/usr/bin/env python3
from finance import create_asset, Indicators, Simulator, Strategy, Trainer, Utils

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

def main():
    symbols = get_symbols()
    indicators = [Indicators.PSAR(), Indicators.EMA(2), Indicators.EMA(20), Indicators.EMA(40), Indicators.EMA(200)]

    # Trainer.create_pickled_assets(symbols, "1d", ASSETS_PICKLE)

    trainer = Trainer(indicators)

    # trainer.load_data(TRAINER_PICKLE)

    trainer.generate_data(saved_assets=ASSETS_PICKLE)
    # trainer.generate_data(symbols=symbols)

    trainer.create_model()
    trainer.train()  # https://www.youtube.com/watch?v=5dx3XD46fE0
    trainer.save_data(TRAINER_PICKLE)

    # print(trainer.predict(trainer.input_train[1], preprocessed=True))

    symbol = "ADA-USD"
    timeframe = "1d"

    asset = create_asset(symbol, timeframe=timeframe)

    start = asset.close.start_date
    end = asset.close.end_date

    cash = asset.get_price_by_date(start)

    s = Simulator(strategy=Strategy.NeuralNetwork([symbol], trainer), start_date=start, end_date=end, timeframe=timeframe, cash=cash)
    s.run()
    s.plot(plot_assets=True)


if __name__ == "__main__":
    main()
