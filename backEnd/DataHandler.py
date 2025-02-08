from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
import asyncio
import json
import websockets
import time
from datetime import datetime
from collections import deque

class BinanceDataHandler:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.binanceWsUrl = "wss://stream.binance.com:443/stream?streams=btcusdt@trade/solusdt@trade/ethusdt@trade"
        self.latestTrades = {"BTCUSDT": deque(maxlen=100), "ETHUSDT": deque(maxlen=100), "SOLUSDT": deque(maxlen=100)}
        self.latestKlines = {"BTCUSDT": deque(maxlen=600), "ETHUSDT": deque(maxlen=600), "SOLUSDT": deque(maxlen=600)}  # 10 min of 1s klines
    
    async def connect(self):
        async with websockets.connect(self.binanceWsUrl) as ws:
            print("Connected to Binance WebSocket")
            await self.subscribe(ws)
            await self.listen(ws)
    
    async def subscribe(self, ws):
        subscribeMessage = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@kline_1s", "ethusdt@kline_1s", "solusdt@kline_1s"],
            "id": 1
        }
        await ws.send(json.dumps(subscribeMessage))
        print(f"Subscription response: {await ws.recv()}")
    
    async def listen(self, ws):
        try:
            while True:
                message = json.loads(await ws.recv())
                self.processMessage(message)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"Error in listen loop: {e}")
    
    def processMessage(self, message):
        if 'data' not in message:
            return
        stream, data = message['stream'], message['data']
        symbol = stream.split('@')[0].upper()
        
        if '@trade' in stream:
            tradeInfo = {
                "price": float(data['p']),
                "quantity": float(data['q']),
                "timestamp": int(data['T'])
            }
            self.latestTrades[symbol].append(tradeInfo)
            print(symbol, " trade")
            # Check price change
            if len(self.latestTrades[symbol]) > 1:
                if self.latestTrades[symbol][-2]['price'] != self.latestTrades[symbol][-1]['price']:
                    # self.socketio.emit("tradeUpdate", self.latestTrades[symbol], broadcast=True)
                    self.printTrade(symbol)
        elif '@kline' in stream:
            klineInfo = {
                "open": float(data['k']['o']),
                "high": float(data['k']['h']),
                "low": float(data['k']['l']),
                "close": float(data['k']['c']),
                "volume": float(data['k']['v']),
                "trades": int(data['k']['n']),
                "timestamp": int(data['k']['t'])
            }
            self.latestKlines[symbol].append(klineInfo)
            self.printKline(symbol)
            self.socketio.emit("newCandle", {symbol, self.latestKlines[symbol]}, broadcast=True)
    
    def printTrade(self, symbol):
        trade = self.latestTrades[symbol][-1]
        print(f"{symbol} Trade - Price: ${trade['price']}, Quantity: {trade['quantity']}, Time: {datetime.fromtimestamp(trade['timestamp'] / 1000)}")
    
    def printKline(self, symbol):
        kline = self.latestKlines[symbol][-1]
        print(f"{symbol} Kline - Open: ${kline['open']}, High: ${kline['high']}, Low: ${kline['low']}, Close: ${kline['close']}, Volume: {kline['volume']}, Trades: {kline['trades']}")
    
    def getLatestTrade(self, symbol):
        return self.latestTrades[symbol][-1] if self.latestTrades[symbol] else None
    
    def getLatestKline(self, symbol):
        return self.latestKlines[symbol][-1] if self.latestKlines[symbol] else None
    
    def getCachedKlines(self, symbol):
        return self.latestKlines[symbol]

async def main():
    handler = BinanceDataHandler()
    await handler.connect()

if __name__ == "__main__":
    asyncio.run(main())