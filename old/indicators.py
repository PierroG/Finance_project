import numpy as np
import pandas as pd

import yfinance as yf
import math
# -- Indicator --
#Simple Moving Average
def SMA(data, span = 10):
    return data.rolling(window = span).mean()

#Exponential Moving Average
def EMA(data, span = 10):
    return data.ewm(span = span, adjust = False).mean()

# Triple Exponential Moving Average
def TEMA(data, span):
    EMA1 = EMA(data, span=span)
    EMA2 = EMA(EMA1, span=span)
    EMA3 = EMA(EMA2, span=span)
    TEMA = (3*EMA1) - (3*EMA2) + EMA3
    return TEMA

def MACD(data):
    macd = EMA(data, span=12) - EMA(data, span=26)
    return macd
    
def momentum(data, span = 4):
    return data.pct_change(span)

def momentum2(data, span = 4):
    return data.diff(span)

def volatility_pd(data):
    mean = data.mean()
    a = (data - mean)**2
    vol = math.sqrt(a.sum()/len(data))
    print(vol/mean)
    return vol/mean

def ATR(data):
    for data_point in data:
        curr = max(curr_hig - curr_low, abs(curr_hig - prev_low), abs(curr_low - prev_low))
# --------------------------------
def pct_of(num, pct):
    """
        compute pourcentage of a value
    """
    value = num * (pct/100)
    #print('> ' + str(pct) + "% of " + str(num)+ " is : " + str(value))     ▲ ▼ 
    return value

def pct_change(first_num, second_num):
    """
        Compute pourcentage of changes between two number
    """
    diff = second_num - first_num    
    pct = (diff / first_num) *100
    return pct

def print_pct(pct):
    if pct > 0:
        return color.GREEN + " {:.2f}".format(pct) + ' %' + ' ▲' + color.END
    elif pct < 0:
        return color.RED + "{:.2f}".format(pct) + ' %' + ' ▼'+ color.END
    else:
        return color.YELLOW + " " + str(pct) + ' %' + color.END

# --------------------------------
def printa():
    print('b')

def get_historic_data(pair_name, period = '7d', interval='30m', start=None, end=None):
    ticker = yf.Ticker(pair_name) #ETH - BTC #XLM #ETH-EUR
    if start is not None:
        data = ticker.history(start=start, end=end, interval=interval) #period="7d", interval="5m", start="2021-04-19", end="2021-04-25"
        return data
    else: 
        data = ticker.history(period= period, interval=interval)
        return data

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'