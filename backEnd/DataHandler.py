import asyncio
import json
import websockets
import time
from datetime import datetime
from collections import deque

class BinanceDataHandler:
    def __init__(self):
        self.BINANCE_WS_URL = "wss://stream.binance.com:443/stream?streams=btcusdt@trade/solusdt@trade/ethusdt@trade"
        self.latest_trades = {"BTCUSDT": deque(maxlen=100), "ETHUSDT": deque(maxlen=100), "SOLUSDT": deque(maxlen=100)}
        self.latest_klines = {"BTCUSDT": deque(maxlen=600), "ETHUSDT": deque(maxlen=600), "SOLUSDT": deque(maxlen=600)}  # 10 min of 1s klines
    
    async def connect(self):
        async with websockets.connect(self.BINANCE_WS_URL) as ws:
            print("Connected to Binance WebSocket")
            await self.subscribe(ws)
            await self.listen(ws)
    
    async def subscribe(self, ws):
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@kline_1s", "ethusdt@kline_1s", "solusdt@kline_1s"],
            "id": 1
        }
        await ws.send(json.dumps(subscribe_message))
        print(f"Subscription response: {await ws.recv()}")
    
    async def listen(self, ws):
        try:
            while True:
                message = json.loads(await ws.recv())
                self.process_message(message)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"Error in listen loop: {e}")
    
    def process_message(self, message):
        if 'data' not in message:
            return
        stream, data = message['stream'], message['data']
        symbol = stream.split('@')[0].upper()
        
        if '@trade' in stream:
            trade_info = {
                "price": float(data['p']),
                "quantity": float(data['q']),
                "timestamp": int(data['T'])
            }
            self.latest_trades[symbol].append(trade_info)
            print(symbol," trade")
            #check price change
            if len(self.latest_trades[symbol]) > 1:
                if self.latest_trades[symbol][-2]['price'] != self.latest_trades[symbol][-1]['price']:
                    self.print_trade(symbol)
        elif '@kline' in stream:
            kline_info = {
                "open": float(data['k']['o']),
                "high": float(data['k']['h']),
                "low": float(data['k']['l']),
                "close": float(data['k']['c']),
                "volume": float(data['k']['v']),
                "trades": int(data['k']['n']),
                "timestamp": int(data['k']['t'])
            }
            self.latest_klines[symbol].append(kline_info)
            self.print_kline(symbol)
    
    def print_trade(self, symbol):
        trade = self.latest_trades[symbol][-1]
        print(f"{symbol} Trade - Price: ${trade['price']}, Quantity: {trade['quantity']}, Time: {datetime.fromtimestamp(trade['timestamp'] / 1000)}")
    
    def print_kline(self, symbol):
        kline = self.latest_klines[symbol][-1]
        print(f"{symbol} Kline - Open: ${kline['open']}, High: ${kline['high']}, Low: ${kline['low']}, Close: ${kline['close']}, Volume: {kline['volume']}, Trades: {kline['trades']}")

    def get_latest_trade(self, symbol):
        return self.latest_trades[symbol][-1] if self.latest_trades[symbol] else None
    
    def get_latest_kline(self, symbol):
        return self.latest_klines[symbol][-1] if self.latest_klines[symbol] else None
    
    def get_cached_klines(self, symbol):
        return self.latest_klines[symbol]

async def main():
    handler = BinanceDataHandler()
    await handler.connect()

if __name__ == "__main__":
    asyncio.run(main())