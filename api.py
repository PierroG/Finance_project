from typing import List
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from binance.client import Client
from binance import BinanceSocketManager, AsyncClient
from enum import Enum

from fastapi.middleware.cors import CORSMiddleware

from functools import lru_cache
from cachetools import cached, TTLCache

import time

app = FastAPI()

origins = [
    "*"
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Interval(str, Enum):
    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'

# Binance API credentials
API_KEY = 'gK0Ubnyg0Vzo8xz4AUElk8I1BitzDGMwn5o9392eko3SiltDDf5Sl0ySKM6bqLyT'
API_SECRET = 'bbPcOuBvYVtXQaNYXKboPWPSHDXd9BzZV16OyygOSUMt0sA1NqMTkWT0gLZ4aUvl'

# Create an in-memory cache with a time-to-live (TTL) of 1 hour
cache = TTLCache(maxsize=100, ttl=3600)


client = Client(API_KEY, API_SECRET)
# bsm = BinanceSocketManager(client)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tickers")
def get_tickers():
    info = client.get_symbol_info('BNBBTC')
    print(info)
    prices = client.get_all_tickers()
    return prices

@cached(cache)
def get_historical_data(symbol, interval): # stock_symbol, start_date, end_dat
    candles = client.get_historical_klines(symbol=symbol,
                                           interval=interval)
    print(len(candles))
    return candles

@app.get("/stocks/{symbol}/historical-data")
def historic_request(symbol: str, interval: Interval = Interval.KLINE_INTERVAL_1DAY):
    """
    Response:
    [
        [
            1499040000000,      // Kline open time
            "0.01634790",       // Open price
            "0.80000000",       // High price
            "0.01575800",       // Low price
            "0.01577100",       // Close price
            "148976.11427815",  // Volume
            1499644799999,      // Kline Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "0"                 // Unused field, ignore.
        ]
    ]
    """
    print(f"request historical {symbol} with interval: {interval.value}")
    # candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, startTime='"1 Jan, 2017"')
    # candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "1 Apr, 2023")
    candles = get_historical_data(symbol, interval.value)

    return candles

import talib
import numpy as np
import json

@app.get("/stocks/{symbol}/indicators/{indicator_name}")
def historic_request(symbol: str, indicator_name: str, option = {}, interval: Interval = Interval.KLINE_INTERVAL_1DAY):
    option = json.loads(option) # Load option dictionary
    print(f"request indecators <{indicator_name}> for symbol <{symbol}> with param: <{option}>")
    data = get_historical_data(symbol, interval.value) # retreive Data
    close_data =  np.array([float(elem[1]) for elem in data])

    sma = talib.SMA(close_data,**option)
    sma = np.where(np.isnan(sma), None, sma)
    # Format data
    output = []
    for sm, dat in zip(sma, data):
        if sm:
            output.append({'time': dat[0]/1000, 'value': sm })
    return output

@app.websocket("/realtime/{symbol}")
async def websocket_endpoint(symbol: str, websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()

    bsm = BinanceSocketManager(client)

    def process_data(data):
        print(data)

     # start any sockets here, i.e a trade socket
    ts = bsm.kline_socket(symbol)
    
    async def send_data_to_websocket(msg):
        await websocket.send_text(str(msg))

    async with ts as tscm:
        while True:
            try:
                data = await tscm.recv()
                print(data)
                await send_data_to_websocket(data)
            
            except Exception as e:
                print("Exception catched")
                break
                
    # then start receiving messages
    # async with ts as tscm:
    #     while True:
    #     # try:
    #         # res = await tscm.recv()
    #         res = await tscm.recv()
    #         print(res)
    #         # print(res)
    #     except WebSocketDisconnect:
    #         print('error WebSocketDisconnect')

    #     except Exception as e:
    #         print('error:', e)
    #         break
        # WebSocket disconnected, stop the BinanceSocketManager connection
        # print("frontend socket disconect")
        # bsm.stop_socket(ts)
        # bsm.close()
    print('end of socket..')

    # await client.close_connection()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=6500, reload=True)


# Working socket format

# while True:
#     try:
#         # res = await tscm.recv()
#         data = await websocket.receive_text()
#         # print(res)
#     except WebSocketDisconnect:
#         print('error WebSocketDisconnect')

#     except Exception as e:
#         print('error:', e)
#         break