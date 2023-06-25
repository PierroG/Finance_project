class TradingBot:
    def __init__(self, api_key, api_secret, symbol, quantity, interval):
        self.client = Client(api_key, api_secret)
        self.strategy = None
        self.symbol = symbol
        self.quantity = quantity
        self.interval = interval
        self.data_manager = DataManager(self.client)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def run_live(self):
        while True:
            try:
                # Fetch real-time data
                data = self.data_manager.get_real_time_data(self.symbol, self.interval)

                # Generate signal using the strategy
                if self.strategy.generate_signal(data):
                    self.place_market_buy_order(self.symbol, self.quantity)

                # Wait for the next candle
                time.sleep(60)
            except Exception as e:
                print(f"An error occurred: {e}")

    def backtest(self, start_date, end_date):
        # Fetch historical data
        data = self.data_manager.get_historical_data(self.symbol, self.interval, start_date, end_date)

        for candle in data:
            if self.strategy.generate_signal(candle):
                print(f"Buy order triggered at {candle[0]}")

    def place_market_buy_order(self, symbol, quantity):
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            print(f"Buy order placed: {order}")
        except Exception as e:
            print(f"An error occurred: {e}")

class Strategy:
    def __init__(self):
        """"""
        # Initialize any strategy-specific parameters or indicators

    def generate_signal(self, data):
        """"""
        # Implement the strategy logic here
        # Given the input data, generate a buy/sell signal
        # Return True for buy signal, False for sell signal

    # Other methods specific to the strategy

class BasicStrategy:
    def __init__(self):
        self.indicators = {}

    def generate_signal(self, data):
        ...

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

from binance.client import Client

class BinanceDataSource(DataSource):
    def __init__(self, api_key, api_secret):
        self.client =  Client(api_key, api_secret)

    def get_historical_data(self,symbol, interval, start_date, end_date):
        candles = self.client.get_historical_klines(symbol=symbol,
                                                    interval=interval)
    

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

import time

class UniformRandomData():

    def get_data(self):
        import random
        
        price = 100
        for i in range(100):
            random_value = random.uniform(0, 1)*2 - 1
            price += random_value
            return price


class DataStreamingTest(DataTest):

    def get_data(self):
        for i in range(100):
            time.sleep(.5)
            yield i

dataSource = DataStreamingTest()

for elem in dataSource.get_data():
    print(elem)
