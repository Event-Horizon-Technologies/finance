#!/usr/bin/python
from finance import Asset, Indicators, Simulator, Strategy, Trainer, Utils

import numpy as np
import sys

def main(argv):
    symbol    = argv[0] if len(argv) > 0 else "BTC-USD"
    timeframe = argv[1] if len(argv) > 1 else "1d"

    trainer = Trainer()
    trainer.generate_data(["BTC-USD", "ETH-USD"], [Indicators.PSAR(), Indicators.EMA(20), Indicators.EMA(40)])
    trainer.create_model()
    trainer.train()  # https://www.youtube.com/watch?v=5dx3XD46fE0

if __name__ == "__main__":
    main(sys.argv[1:])
