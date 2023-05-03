
class NotEnoughCash(Exception):
    """ """
class NotEnoughToken(Exception):
    """ """

import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # to remove pandas warning # TODO fix the warning
import yfinance as yf
import matplotlib.pyplot as plt
import indicators as indic

class FinanceBotTest():
    """ """

    def __init__(self,
                 pair: str,
                 cash: int = 0,
                 cash_currency: str = '$',
                 token: int = 0,
                 trade_fees: int = 0
                 ) -> None:
        self.pair = pair # base currency / quote currency (crypto-currency or fiat-curency)
        self.cash = cash
        self.cash_currency = cash_currency
        self.token = token
        self.trade_fees = trade_fees

        self.buy_data = pd.DataFrame()
        self.sell_data = pd.DataFrame()

    def get_ticker_from_pair(self, pair):
        pair = pair.replace('/', '-').replace('_', '-').upper()
        ticker = yf.Ticker(pair)
        return ticker

    def get_historic_data(self, pair_name, period = '7d', interval='30m', start=None, end=None) -> pd.DataFrame:
        ticker = yf.Ticker(pair_name) #ETH - BTC #XLM #ETH-EUR
        if start is not None:
            data = ticker.history(start=start, end=end, interval=interval) #period="7d", interval="5m", start="2021-04-19", end="2021-04-25"
            return data
        else: 
            data = ticker.history(period= period, interval=interval)
            return data

    def buy(self, index, row, rate=None, money=None) -> None:
        # TODO add fees
        if (self.cash - money >= 0): # be sure that the money is availabe
            self.cash = self.cash - money
            self.token = money / rate
            self.buy_data = self.buy_data.append({'Datetime': index, 'Close': row['Close']}, ignore_index=True)
        else: raise NotEnoughCash

    def sell(self, index, row, rate=None, token=None) -> None: 
        """
        args:
            - rate ~ price (how much monney for one token/share)
        """ 
        # TODO add fees
        if (self.token - token >= 0): # be sure that the money is availabe
            self.token = self.token - token
            self.cash = token * rate
            self.sell_data = self.sell_data.append({'Datetime': index, 'Close': row['Close']}, ignore_index=True)
        else: raise NotEnoughCash

    def should_buy(self, index, row) -> bool:
        return True

    def should_sell(self, index, row) -> bool:
        return True

    def compute(self, data) -> pd.DataFrame:
        print("_compute_")
        data['tema'] = indic.SMA(data['Close'], span = 200)
        data['sma'] = indic.EMA(data['Close'], span = 50)
        data['ss'] = indic.EMA(data['Close'], span = 1)
        return data

    def main_loop(self) -> None:
        """ should fetch data
        process data
        check buy / sell condition
        log
        log + chart at the end
        """
        for index, row in self.data.iterrows():
            if self.should_buy(index, row):
                self.buy(index, row, rate=row['Close'], money=self.cash)
            if self.should_sell(index, row):
                self.sell(index, row, rate=row['Close'], token=self.token)

    def chart(self):
        self.buy_data.set_index('Datetime', inplace=True)
        self.sell_data.set_index('Datetime', inplace=True)
        plt.close('all')

        fig = plt.figure(figsize=(16,12))

        #Define subplot
        ax1 = plt.subplot2grid((1,1), (0,0), rowspan=4, colspan=1)
        # ax2 = plt.subplot2grid((6,1), (4,0), rowspan=1, colspan=1, sharex=ax1)
        # ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

        #Create plots
        ax1.plot(self.data['Close'], linewidth=0.8)
        ax1.plot(self.data['tema'], linewidth=0.8)
        ax1.plot(self.data['sma'], linewidth=0.8)

        ax1.scatter(self.sell_data.index, self.sell_data['Close'], c = 'red', marker = 8, s = 30, alpha=1)
        ax1.scatter(self.buy_data.index, self.buy_data['Close'], c = 'green', marker = 9, s = 30, alpha=1)

        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        plt.show()

    def log_wallet(self):
        ...

    def log_gain(self):
        ...

    def __str__(self) -> str:
        """ special methods called by print """
        return "test"
    
    def run(self) -> None:
        # self.ticker = self.get_ticker_from_pair(pair)
        self.data = self.get_historic_data(self.pair)
        print(self.data.head())
        self.data = self.compute(self.data)
        self.main_loop()
        self.chart()

Ft = FinanceBotTest(
    pair= "ETH-USD",
    cash=1000,
    cash_currency='$',
    trade_fees=0
)
Ft.run()
