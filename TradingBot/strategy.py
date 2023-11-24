from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, buy_callback=None, sell_callback=None):
        """"""
        # Initialize any strategy-specific parameters or indicators
        self.indicators = {}

        self.buy_callback = buy_callback or (lambda: print('buy'))
        self.sell_callback = sell_callback or (lambda: print('sell'))

    @abstractmethod
    def should_buy(self, data):
        ...

    @abstractmethod
    def should_sell(self, data):
        ...

    @abstractmethod
    def generate_signal(self, data):
        """"""
        # Implement the strategy logic here
        # Given the input data, generate a buy/sell signal
        # Return True for buy signal, False for sell signal
        if self.should_buy():
            self.buy_callback()

        if self.should_sell():
            self.sell_callback()

    def compute_indicators(self, data, elem):
        """ """
        # Other methods specific to the strategy

import talib
import numpy
import numpy as np
# from talib import stream
from utils import sstream

class SimpleStrategy(Strategy):
    def __init__(self):
        self.indicators = {}

    def compute_indicators(self, data, elem=None):
        np_data = np.array([e['Close'] for e in data])
        # SMA
        data[-1]['SMA'] = sstream('SMA', np_data, timeperiod=12) #talib require np array
        # EMA
        data[-1]['TEMA'] = sstream('DEMA', np_data, timeperiod=12) #talib require np array


    def should_buy(self, data):
        pass

    def should_sell(self, data):
        pass

    def generate_signal(self, data):
        self.compute_indicators(data)
        return []

if __name__ == "__main__":

    st = SimpleStrategy()
