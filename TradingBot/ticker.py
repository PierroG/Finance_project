from enum import Enum

import yfinance as yf

# Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

# valid intervals 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
class Interval(Enum):
    pass

class YahooTicker:
    def __init__(self, symbol, interval):
        self.symbol = symbol.upper()  # "ETH-USD"
        self.interval = interval

        self.ticker = yf.Ticker(self.symbol)


    def get_historical_data(self, period=None, start_date=None, end_date=None):
        """date string YYYY-MM-DD or datetime object"""
        data = self.ticker.history(period=period, interval=self.interval, start=start_date, end=end_date) #period="7d", interval="5m"
        data['timestamp'] = data.index  # .strftime('%Y-%m-%d %X')
        # or data.reset_index()
        for i in data.to_dict('records'):
            yield i


if __name__ == "__main__":
    yt = YahooTicker("ETH-USD", "5m")
    for elem in yt.get_historical_data("1d"):
        print(elem)