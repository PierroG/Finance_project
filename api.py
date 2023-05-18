from typing import List
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from binance.client import Client
from binance import BinanceSocketManager, AsyncClient

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

# Binance API credentials
API_KEY = 'gK0Ubnyg0Vzo8xz4AUElk8I1BitzDGMwn5o9392eko3SiltDDf5Sl0ySKM6bqLyT'
API_SECRET = 'bbPcOuBvYVtXQaNYXKboPWPSHDXd9BzZV16OyygOSUMt0sA1NqMTkWT0gLZ4aUvl'

# Create an in-memory cache with a time-to-live (TTL) of 1 hour
cache = TTLCache(maxsize=100, ttl=3600)


client = Client(API_KEY, API_SECRET)
# bsm = BinanceSocketManager(client)

@app.get("/")
def read_root(x: int):
    get_historical_dataa('BNBBTC')
    print(cache)
    return {"Hello": "World"}

@app.get("/tickers")
def get_tickers():
    info = client.get_symbol_info('BNBBTC')
    print(info)
    prices = client.get_all_tickers()
    return prices

@cached(cache)
def get_historical_dataa(symbol): # stock_symbol, start_date, end_dat
    candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "1 Apr, 2023")

    return candles

@app.get("/historical/{symbol}")
def historic_request(symbol: str, interval=None):
    print(f"request historical {symbol}")
    interval = ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h",
    "1d", "3d", "1w", "1M"),
    # candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, startTime='"1 Jan, 2017"')
    candles = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "1 Apr, 2023")
    
    # Process the candles as needed
    return candles

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