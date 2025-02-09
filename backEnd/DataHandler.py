from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
import asyncio
import json
import websockets
import time
from datetime import datetime
import Database
from GameManager import Game


class BinanceDataHandler:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.binanceWsUrl = "wss://stream.binance.com:443/stream?streams=btcusdt@trade/solusdt@trade/ethusdt@trade"
        self.latestTrades = {"BTCUSDT": {}, "ETHUSDT": {}, "SOLUSDT": {}}
        self.latestKlines = {"BTCUSDT": {}, "ETHUSDT": {}, "SOLUSDT": {}}
        self.maxTrades = 100
        self.maxKlines = 600  # 10 min of 1s klines
        self.mostRecentTimestamp = 0
        self.numOfSymbolsRecieved = 0
        self.games = {}
        self.createGame("99999", 50)
        self.games["99999"].addUser("12345")

    def createGame(self, gameId, entryFee):
        self.games[gameId] = (Game(self.socketio, gameId, entryFee))

    def endGame(self, gameId):
        winner = self.games[gameId].getWinner()
        # update winner's balance
        Database.addGems(winner, self.games[gameId].getJackpot())
        del self.games[gameId]

    def getGame(self, gameId):
        return self.games[gameId]

    def updateCryptoPrice(self, btc, eth, sol):
        # Check if game is still active
        for gameId, game in self.games.items():
            if time.time() < game.timeFinish:
                game.updateCryptoPrice(btc, eth, sol)
                
            elif time.time() >= game.timeFinish:
                self.endGame(gameId)

    def editPosition(self, gameId, userId, symbol, margin, leverage):
        self.games[gameId].editPosition(userId, symbol, margin, leverage) # fix

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
            # print(symbol, " trade")
            # Check price change
            if len(self.latestTrades[symbol]) > 1:
                timestamps = sorted(self.latestTrades[symbol].keys())
                if self.latestTrades[symbol][timestamps[-2]]['price'] != self.latestTrades[symbol][timestamps[-1]][
                    'price']:
                    pass
                    # self.socketio.emit("tradeUpdate", self.latestTrades[symbol])
                    # self.printTrade(symbol)
        elif '@kline' in stream:
            klineInfo = {
                "time": int(data['k']['t']) / 1000,
                "open": float(data['k']['o']),
                "close": float(data['k']['c']),
                "high": float(data['k']['h']),
                "low": float(data['k']['l'])
            }
            self.latestKlines[symbol][klineInfo['time']] = klineInfo
            self.trimDict(self.latestKlines[symbol], self.maxKlines)
            if klineInfo['time'] > self.mostRecentTimestamp:
                self.mostRecentTimestamp = klineInfo['time']
                self.numOfSymbolsRecieved = 1
            elif klineInfo['time'] == self.mostRecentTimestamp:
                self.numOfSymbolsRecieved += 1
            if self.numOfSymbolsRecieved >= 3:
                self.numOfSymbolsRecieved -= 3
                print("3 symbols recieved")
                self.socketio.emit("newCandle", {
                    "BTCUSDT": list(self.latestKlines["BTCUSDT"].values())[-1],
                    "ETHUSDT": list(self.latestKlines["ETHUSDT"].values())[-1],
                    "SOLUSDT": list(self.latestKlines["SOLUSDT"].values())[-1]
                })
                for game in self.games.values():
                    game.updateCryptoPrice(list(self.latestKlines["BTCUSDT"].values())[-1]["close"], list(self.latestKlines["ETHUSDT"].values())[-1]["close"], list(self.latestKlines["SOLUSDT"].values())[-1]["close"])
                    self.emitUserStates()
                    print("emitted user states")

    def trimDict(self, dictionary, maxLength):
        while len(dictionary) > maxLength:
            oldest_key = min(dictionary.keys())
            del dictionary[oldest_key]

    def printTrade(self, symbol):
        trade = list(self.latestTrades[symbol].values())[-1]
        print(
            f"{symbol} Trade - Price: ${trade['price']}, Quantity: {trade['quantity']}, Time: {datetime.fromtimestamp(trade['timestamp'] / 1000)}")

    def printKline(self, symbol):
        kline = list(self.latestKlines[symbol].values())[-1]
        print(
            f"{symbol} Kline - Open: ${kline['open']}, High: ${kline['high']}, Low: ${kline['low']}, Close: ${kline['close']}")

    def getLatestTrade(self, symbol):
        return list(self.latestTrades[symbol].values())[-1] if self.latestTrades[symbol] else None

    def getLatestKline(self, symbol):
        return list(self.latestKlines[symbol].values())[-1] if self.latestKlines[symbol] else None

    def getCachedKlines(self, symbol):
        return list(self.latestKlines[symbol].values())

    def emitUserStates(self):
        for gameId, game in self.games.items():
            game.emitUserState()

    def addUserToGame(self, gameId, userId):
        game = self.games[gameId]
        if Database.checkNumOfGems(userId) >= game.entryFee:
            game.addUser(userId)
            Database.addGems(userId, -1 * game.entryFee)


async def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jrhbieygfhcbvhwruygv32rughf123ttrplace1beuygfreoubvwro'
    socketio = SocketIO(app, ping_timeout=5, ping_interval=15, logger=True, engineio_logger=True)
    handler = BinanceDataHandler(socketio)
    await handler.connect()


if __name__ == "__main__":
    asyncio.run(main())