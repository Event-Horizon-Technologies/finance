from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, symbols=None, indicators=None):
        self.symbols = symbols
        self.indicators = indicators

    @abstractmethod
    def strategy(self, simulator):
        return {}
