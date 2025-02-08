from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
import asyncio
import json
import websockets
import time
from datetime import datetime

class BinanceDataHandler:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.binanceWsUrl = "wss://stream.binance.com:443/stream?streams=btcusdt@trade/solusdt@trade/ethusdt@trade"
        self.latestTrades = {"BTCUSDT": {}, "ETHUSDT": {}, "SOLUSDT": {}}
        self.latestKlines = {"BTCUSDT": {}, "ETHUSDT": {}, "SOLUSDT": {}}  # 10 min of 1s klines
        self.maxTrades = 100
        self.maxKlines = 600
    
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
            self.latestTrades[symbol][tradeInfo['timestamp']] = tradeInfo
            self.trimDict(self.latestTrades[symbol], self.maxTrades)
            print(symbol, " trade")
            # Check price change
            if len(self.latestTrades[symbol]) > 1:
                timestamps = sorted(self.latestTrades[symbol].keys())
                if self.latestTrades[symbol][timestamps[-2]]['price'] != self.latestTrades[symbol][timestamps[-1]]['price']:
                    self.socketio.emit("tradeUpdate", self.latestTrades[symbol], broadcast=True)
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
            self.latestKlines[symbol][klineInfo['timestamp']] = klineInfo
            self.trimDict(self.latestKlines[symbol], self.maxKlines)
            self.printKline(symbol)
            self.socketio.emit("newCandle", {"symbol": symbol, "klines": list(self.latestKlines[symbol].values())}, broadcast=True)
    
    def trimDict(self, dictionary, maxLength):
        while len(dictionary) > maxLength:
            oldest_key = min(dictionary.keys())
            del dictionary[oldest_key]
    
    def printTrade(self, symbol):
        trade = list(self.latestTrades[symbol].values())[-1]
        print(f"{symbol} Trade - Price: ${trade['price']}, Quantity: {trade['quantity']}, Time: {datetime.fromtimestamp(trade['timestamp'] / 1000)}")
    
    def printKline(self, symbol):
        kline = list(self.latestKlines[symbol].values())[-1]
        print(f"{symbol} Kline - Open: ${kline['open']}, High: ${kline['high']}, Low: ${kline['low']}, Close: ${kline['close']}, Volume: {kline['volume']}, Trades: {kline['trades']}")
    
    def getLatestTrade(self, symbol):
        return list(self.latestTrades[symbol].values())[-1] if self.latestTrades[symbol] else None
    
    def getLatestKline(self, symbol):
        return list(self.latestKlines[symbol].values())[-1] if self.latestKlines[symbol] else None
    
    def getCachedKlines(self, symbol):
        return list(self.latestKlines[symbol].values())

async def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jrhbieygfhcbvhwruygv32rughf123ttrplace1beuygfreoubvwro'
    socketio = SocketIO(app, ping_timeout=5, ping_interval=15, logger=True, engineio_logger=True)
    handler = BinanceDataHandler(socketio)
    await handler.connect()

if __name__ == "__main__":
    asyncio.run(main())