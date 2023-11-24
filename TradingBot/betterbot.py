
from ticker import YahooTicker
from strategy import SimpleStrategy
import matplotlib.pyplot as plt

import pandas as pd


class Bot:
    def __init__(self) -> None:
        
        self.ticker = YahooTicker(symbol='ETH-USD',
                                  interval='5m')
        
        self.strategy = SimpleStrategy()
        self.trades = []

    def run(self):
        self.data = []
        for tick in self.ticker.get_historical_data(period='1d'):
            self.data.append(tick)

            signals = self.strategy.generate_signal(self.data)

            for signal in signals:
                if signal['type'] == 'buy':
                    self.buy()
                if signal['type'] == 'sell':
                    self.sell()

        # print(self.data)
    # TODO - Shoud be handle in Exchange class ?
    def buy(self, price):
        self.trades.append({'type': 'buy', 'price': price})
    
    def sell(self, price):
        self.trades.append({'type': 'sell', 'price': price})

    def get_report(self):
        print(self.trades)

    def plot(self):
        df = pd.DataFrame(self.data)

        plt.close('all')
        fig = plt.figure(figsize=(16,8))

        #Define subplot
        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
        # ax2 = plt.subplot2grid((6,1), (4,0), rowspan=1, colspan=1, sharex=ax1)
        # ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

        #Create plots
        ax1.plot(df['Close'], linewidth=0.8)
        ax1.plot(df['SMA'], linewidth=0.8)
        ax1.plot(df['TEMA'], linewidth=0.8)
        
        # sell = [trade for trade]
        # ax1.scatter(sell.index, sell['Close'], c = 'red', marker = 8, s = 30, alpha=1)
        # ax1.scatter(buy.index, buy['Close'], c = 'green', marker = 9, s = 30, alpha=1)


        ax1.grid(alpha=0.3)
        plt.tight_layout()

        plt.show()

if __name__ == "__main__":
    bot = Bot()
    bot.run()
    bot.get_report()
    bot.plot()