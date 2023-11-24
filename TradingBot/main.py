from bot import TradingBot, Strategy
import numpy as np

import talib
from talib import stream

import random

from typing import List, Dict, Text

class MyStrat(Strategy):

    def generate_signal(self, data):
        """"""
        rand = random.uniform(0,1)
        if rand < 0.2:
            return True
        return False

    def compute_indicators(self, past_data: List[Dict], current_elem: Dict):
        """"""
        close = np.array([e['Close'] for e in past_data])
        current_elem['sma_5'] = stream.SMA(close, timeperiod=5)
        current_elem['sma_10'] = stream.SMA(close, timeperiod=5)
        current_elem['macd'] = stream.MACD(close)
        

        return current_elem
    
bot = TradingBot()
strat = MyStrat()
bot.set_strategy(strat)

bot.backtest()