from flask_socketio import SocketIO
from typing import Dict, List
import time


class Game:
    def __init__(self, socket, gameID, entryFee) -> None:
        self.socketio = socket
        self.gameID = gameID
        self.users = []
        self.timeStart = time.time()
        self.timeFinish = time.time() + 180
        self.gameInProgress = True
        self.jackpot = 0
        self.entryFee = entryFee

        self.btcPrice = None
        self.ethPrice = None
        self.solPrice = None
        print("game Created! ")

    def updateCryptoPrice(self, btc, eth, sol):
        self.btcPrice = btc
        self.ethPrice = eth
        self.solPrice = sol
        self.updateUserPortValues()

    def updateUserPortValues(self):
        for user in self.users:
            value = user.updatePortValue([self.btcPrice, self.ethPrice, self.solPrice])
            if value <= 0:
                user.liquidated()

    def editPosition(self, userId, coin, margin, lev):  # maybe do amount maybe margin and lev
        coinPrice = 0
        amount = margin * lev
        # mega shit code below
        if coin == "BTCUSDT":
            coinPrice = self.btcPrice
        if coin == "ETHUSDT":
            coinPrice = self.ethPrice
        if coin == "SOLUSDT":
            coinPrice = self.solPrice
        for user in self.users:
            if user.getUserId() == userId and user.getUserState()["balance"] >= margin:
                user.updatePosition(amount, coin, coinPrice)

    def endGame(self):
        pass

    def calcPNL(self):
        for user in self.users:
            user.updatePortValue([self.btcPrice, self.ethPrice, self.solPrice])

    # Get all details to send to front end
    def getUserState(self, userId):
        for user in self.users:
            if user.getUserId() == userId:
                return user.getUserState()  # balance positions pnl liquidated

    def emitUserState(self):
        output = {}
        for user in self.users:
            output[user.getUserId] = user.getUserState()
        self.socketio.emit(self.gameID + "/gameState", output)


    def addUser(self, userId):
        self.users.append(User(userId, 1000))
        self.jackpot += self.entryFee

    def getWinner(self):
        currentWinner = None
        highestPnl = 0
        for user in self.users:
            pnl = user.updatePortValue([self.btcPrice, self.ethPrice, self.solPrice])
            if highestPnl < pnl:
                highestPnl = pnl
                currentWinner = user.getUserId()
        return currentWinner


class User:
    def __init__(self, userId, startBalance):
        self.balance = startBalance
        self.listPositions = {"BTCUSDT": 0, "ETHUSDT": 0, "SOLUSDT": 0}
        self.userId = userId
        self.debt = 0
        self.pnl = 0
        self.liquidated = False

    def getUserState(self):
        return {"userId": self.userId, "balance": self.balance, "positions": self.listPositions, "pnl": self.pnl,
                "liquidated": self.liquidated}

    def updatePortValue(self, prices):  # must call this to update port value
        value = 0
        for coin, position in self.listPositions.items():
            if coin == "BTCUSDT":
                value += position * prices[0]
            elif coin == "ETHUSDT":
                value += position * prices[1]
            elif coin == "SOLUSDT":
                value += position * prices[2]
        self.pnl = self.balance + value - self.debt
        if self.pnl <= 0:
            self.liquidated = True
        return self.pnl


    def getDebt(self):
        return self.debt

    def addBalance(self, newBalance):
        self.balance += newBalance

    def addDebt(self, addDebt):
        self.debt += addDebt

    def liquidated(self):
        self.liquidated = True

    def getUserId(self):
        return self.userId

    def updatePosition(self, amount, coin, coinPrice):  # coin must be string of either "BTC" "ETH" "SOL"
        numOfCoins = amount / coinPrice
        newCoinAmountMod = abs(self.listPositions[coin] + numOfCoins)
        self.debt += (newCoinAmountMod - self.listPositions[coin]) * coinPrice
        return self.getUserState()