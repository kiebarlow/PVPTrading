from flask_socketio import SocketIO
from typing import Dict, List
import time  
        
class Game:
    def init(self, gameID, users) -> None:
        self.gameID = None
        self.users = []
        self.timeStart = time.now()
        self.timeFinish = time.now() + 180
        self.gameInProgress
        self.jackpot = 0

        self.btcPrice = None
        self.ethPrice = None
        self.solPrice = None

    def updateCryptoPrice(self, data):
        self.btcPrice = data.btcPrice
        self.ethPrice = data.ethPrice
        self.solPrice = data.solPrice

    def updateUserPortValues(self):
        for user in self.users:
            value = user.updatePortValue([self.btcPrice, self.ethPrice, self.solPrice])
            if value <= 0:
                user.liquidated()


    def editPosition(self, userId, coin, margin, lev): # maybe do amount maybe margin and lev
        coinPrice = 0
        amount = margin * lev
        # mega shit code below
        if coin == "BTC":
            coinPrice = self.btcPrice
        if coin == "ETH":
            coinPrice = self.ethPrice
        if coin == "SOL":
            coinPrice = self.solPrice
        for user in self.users:
            if user.getUserId() == userId and user.getUserState()["balance"] >= margin:
                user.updatePosition(amount, coin, coinPrice)

    def endGame(self):
        pass

    def calcPNL(self):
        for user in self.users:
            user.updatePortValue([self.btcPrice,self.ethPrice,self.solPrice])

    #Get all details to send to front end
    def getUserState(self, userId):
        for user in self.users:
            if user.getUserId() == userId:
                return user.getUserState() # balance positions pnl liquidated


    def addUser(self, userId):
        self.users.append(User(userId, 1000))

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
    def init(self, userId, startBalance):
        self.balance = startBalance
        self.listPositions = {"BTC": 0, "ETH": 0, "SOL": 0}
        self.userId = userId
        self.debt = 0
        self.pnl = 0
        self.liquidated = False

    def getUserState(self):
        return {"balance": self.balance, "positions": self.listPositions, "pnl": self.pnl, "liquidated": self.liquidated}

    def updatePortValue(self, prices): # must call this to update port value
        count = 0
        value = 0
        for i in self.listPositions:
            value = value + i * prices[count]
            count += 1
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

    def updatePosition(self, amount, coin, coinPrice): # coin must be string of either "BTC" "ETH" "SOL"
        numOfCoins = amount / coinPrice
        newCoinAmountMod = abs(self.listPositions[coin] + numOfCoins)
        self.debt += (newCoinAmountMod - self.listPositions[coin]) * coinPrice
        return self.getUserState()