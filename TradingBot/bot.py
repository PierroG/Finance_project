import pandas as pd
import matplotlib.pyplot as plt
import datasource as ds

import time

class TradingBot:
    def __init__(self,
                 api_key=None,
                 api_secret=None,
                 symbol=None,
                 quantity=None,
                 interval=None):
        # self.client = Client(api_key, api_secret)
        self.strategy = None
        self.symbol = symbol
        self.quantity = quantity
        self.interval = interval
        self.data_manager = ds.YahooDataSource() #YahooDataSource()

    def set_strategy(self, strategy):
        self.strategy = strategy

    def run_live(self):
        while True:
            try:
                # Fetch real-time data
                data = self.data_manager.get_data()
                # data = self.data_manager.get_real_time_data(self.symbol, self.interval)

                # Generate signal using the strategy
                if self.strategy.generate_signal(data):
                    self.place_market_buy_order(self.symbol, self.quantity)

                # Wait for the next candle
                time.sleep(60)
            except Exception as e:
                print(f"An error occurred: {e}")

    def backtest(self, start_date=None, end_date=None):

        data = []
        buy = []
        sell = []
        # Fetch historical data
        for elem in self.data_manager.get_data():
        # for elem in self.data_manager.get_historical_data(self.symbol, self.interval, start_date, end_date):
            data.append(elem)
            elem = self.strategy.compute_indicators(data, elem)
            data[-1] = elem


           
            if self.strategy.generate_signal(elem):
                buy.append(elem)
                # print(f"Buy order triggered at {elem}")
            
            if self.strategy.generate_signal(elem):
                sell.append(elem)
                # print(f"Buy order triggered at {elem}")

        buy_df = pd.DataFrame(buy)
        buy_df = buy_df.set_index('timestamp')

        sell_df = pd.DataFrame(sell)
        sell_df = sell_df.set_index('timestamp')

        # print(buy_df)
        # print(sell_df)

        df = pd.DataFrame(data)
        df = df.set_index('timestamp')
        self.plot(df, buy_df, sell_df)

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

    def plot(self, data, buy, sell):

        plt.close('all')

        fig = plt.figure(figsize=(16,8))

        #Define subplot
        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
        # ax2 = plt.subplot2grid((6,1), (4,0), rowspan=1, colspan=1, sharex=ax1)
        # ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

        #Create plots
        ax1.plot(data['Close'], linewidth=0.8)
        ax1.plot(data['sma_5'], linewidth=0.8)
        
        ax1.scatter(sell.index, sell['Close'], c = 'red', marker = 8, s = 30, alpha=1)
        ax1.scatter(buy.index, buy['Close'], c = 'green', marker = 9, s = 30, alpha=1)


        ax1.grid(alpha=0.3)
        plt.tight_layout()

        plt.show()



