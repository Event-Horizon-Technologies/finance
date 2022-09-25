#!/usr/bin/python
from finance import Asset, Indicators, Simulator, Strategy, Trainer, Utils

import numpy as np
import sys

def main(argv):
    symbol    = argv[0] if len(argv) > 0 else "BTC-USD"
    timeframe = argv[1] if len(argv) > 1 else "1d"

    trainer = Trainer()
    input_data, target_data = trainer.generate_data(["BTC-USD", "ETH-USD"], [Indicators.EMA(20), Indicators.EMA(40)])

    print(input_data, target_data)

if __name__ == "__main__":
    main(sys.argv[1:])
