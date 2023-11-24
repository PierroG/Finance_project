import time

import numpy as np

from binance.client import Client


class DataSource:
    def __init__(self):
        pass

    def get_real_time_data(self, symbol, interval):
        """"""
        # Fetch real-time candlestick data from the exchange
        # Return the data for further processing

    def get_historical_data(self, symbol, interval, start_date, end_date):
        """"""
        # Fetch historical candlestick data from the exchange
        # Return the data for further processing

    # Other methods for data processing, cleaning, and manipulation

class Ticker:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def get_historical_data(self):
        pass


class BinanceDataSource(DataSource):
    def __init__(self, api_key, api_secret):
        self.client =  Client(api_key, api_secret)


    def get_historical_data(self, symbol, interval, start_date, end_date):
        candles = self.client.get_historical_klines(symbol=symbol,
                                                    interval=interval)


class YahooDataSource(DataSource):
    def __init__(self):
        pass
    
    def get_historical_data(self, symbol, period=None, interval=None, start_date=None, end_date=None):
        ticker = yf.Ticker("ETH-USD")
        data = ticker.history(period="7d", interval="1h") #period="7d", interval="5m"
        data['timestamp'] = data.index
        # or data.reset_index()
        for i in data.to_dict('records'):
            yield i

# Binance API credentials
API_KEY = 'gK0Ubnyg0Vzo8xz4AUElk8I1BitzDGMwn5o9392eko3SiltDDf5Sl0ySKM6bqLyT'
API_SECRET = 'bbPcOuBvYVtXQaNYXKboPWPSHDXd9BzZV16OyygOSUMt0sA1NqMTkWT0gLZ4aUvl'


# import talib
# from talib import stream


class DataTest:
    def __init__(self) -> None:
        pass
    
    def get_data(self):
        for i in range(100):
            yield i


class UniformRandomData(DataTest):

    def get_data(self):
        import random
        
        price = 100
        for i in range(100):
            random_value = random.uniform(0, 1)*2 - 1
            price += random_value
            return price



class GBMData(DataTest):
    """Geometric Brownian Motion"""
    
    def get_data(self):
        #FIXME algo made to compute multiple (M) simulation, should comute only one properly
        # Parameters
        # drift coefficent
        mu = 0.1
        # number of steps
        n = 100
        # time in years
        T = 1
        # number of sims
        M = 1
        # initial stock price
        S0 = 100
        # volatility
        sigma = 0.3

        # calc each time step
        dt = T/n
        # simulation using numpy arrays
        St = np.exp(
            (mu - sigma ** 2 / 2) * dt
            + sigma * np.random.normal(0, np.sqrt(dt), size=(M,n)).T
        )

        # include array of 1's
        St = np.vstack([np.ones(M), St])
        # multiply through by S0 and return the cumulative product of elements along a given simulation path (axis=0). 
        St = S0 * St.cumprod(axis=0)

        for idx, e in enumerate(St):
            sample = {'Close': e[0], 'timestamp': idx}
            yield sample


class DataStreamingTest(DataTest):

    def get_data(self):
        for i in range(100):
            time.sleep(.5)
            yield i
