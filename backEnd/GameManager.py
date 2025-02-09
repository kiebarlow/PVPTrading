from flask_socketio import SocketIO
from typing import Dict, List

class GameManager:
    def __init__(self, socketio):
        self.socketio = socketio
        self.games = {}
    
    def createGame(self, gameId: str, userIds: List[str]):
        self.games[gameId] = Game(self.socketio, gameId, userIds)
    
    def getGame(self, gameId):
        return self.games[gameId]
    
    def updatePnL(self, data):
        for game in self.games.values():
            game.handleNewCandle(game, data)
            
    def openPosition(self, gameId, userId, symbol, margin, leverage):
        self.gameManagers[gameId].openPosition(userId, symbol, margin, leverage)
class Game:
    def __init__(self, socketio: SocketIO, gameId: str, userIds: List[str]):
        self.socketio = socketio
        self.userBalances: Dict[str, float] = {}
        self.userPositions: Dict[str, Dict[str, List[dict]]] = {}  # userId -> symbol -> list of positions
        self.gameId = gameId
        self.latestCandles: Dict[List[dict]] = {}
        for userId in userIds:
            self.userBalances[userId] = 10000
            self.userPositions[userId] = {}
        self.userIds = userIds

    def openPosition(self, userId: str, symbol: str, margin: float, leverage: float):
        if userId not in self.userBalances:
            self.userBalances[userId] = 10000

        if userId not in self.userPositions:
            self.userPositions[userId] = {}

        if symbol not in self.userPositions[userId]:
            self.userPositions[userId][symbol] = []

        tradePrice = self.latestCandles[symbol][-1]["price"]
        quantity = abs(margin * leverage) / tradePrice
        positionType = "long" if margin > 0 else "short"

        if self.userBalances[userId] >= abs(margin):
            self.userBalances[userId] -= abs(margin)
            
            newPosition = {
                "symbol": symbol,
                "type": positionType,
                "quantity": quantity,
                "entryPrice": tradePrice,
                "leverage": leverage,
                "margin": abs(margin)
            }
            
            self.userPositions[userId][symbol].append(newPosition)
            self.emitPortfolioUpdate(userId)
        else:
            self.socketio.emit("error", {
                "userId": userId,
                "gameId": self.gameId,
                "message": "Insufficient balance"
            }, room=self.gameId)

    def calculatePositionPnL(self, position: dict, currentPrice: float) -> float:
        priceDiff = currentPrice - position["entryPrice"]
        if position["type"] == "short":
            priceDiff = -priceDiff
        return priceDiff * position["quantity"] * position["leverage"]

    def handleNewCandle(self, candleData: dict):
        self.latestCandles.append(candleData)
        # pop the first element if the length of the list is greater than 10
        if len(self.latestCandles) > 10:
            self.latestCandles.pop(0)
        
        for symbol, candle in candleData.items():
            currentPrice = candle["close"]  # Use closing price from klineInfo

            for userId in list(self.userPositions.keys()):  # Copy keys to avoid modification during iteration
                if symbol not in self.userPositions[userId]:  
                    continue  # Skip users who don't have positions in this symbol
                
                positions = self.userPositions[userId][symbol]
                remainingPositions = []
                totalPnL = 0

                for position in positions:
                    pnl = self.calculatePositionPnL(position, currentPrice)
                    totalPnL += pnl

                    # Check if the position should be liquidated
                    if (position["type"] == "long" and pnl <= -position["margin"] * position["leverage"]) or \
                    (position["type"] == "short" and pnl <= -position["margin"] * position["leverage"]):
                        self.userBalances[userId] = self.userBalances.get(userId, 0) + position["margin"] + pnl
                    else:
                        remainingPositions.append(position)

                # Update user positions
                if remainingPositions:
                    self.userPositions[userId][symbol] = remainingPositions
                else:
                    del self.userPositions[userId][symbol]
                    if not self.userPositions[userId]:  # Remove user if no positions remain
                        del self.userPositions[userId]

                # Handle account liquidation
                if self.userBalances.get(userId, 0) <= 0:
                    self.handleLiquidation(userId)
                else:
                    self.emitPortfolioUpdate(userId)

    def handleLiquidation(self, userId: str):
        del self.userBalances[userId]
        if userId in self.userPositions:
            del self.userPositions[userId]
            
        self.socketio.emit("liquidation", {
            "userId": userId,
            "gameId": self.gameId
        }, room=self.gameId)

    def calculateTotalPortfolioValue(self, userId: str) -> float:
        if userId not in self.userBalances:
            return 0

        totalValue = self.userBalances[userId]
        
        if userId in self.userPositions:
            for symbol in self.userPositions[userId]:
                currentPrice = self.latestCandles[symbol][-1]["price"]
                for position in self.userPositions[userId][symbol]:
                    totalValue += self.calculatePositionPnL(position, currentPrice)

        return totalValue

    def emitPortfolioUpdate(self, userId: str):
        totalValue = self.calculateTotalPortfolioValue(userId)
        
        self.socketio.emit("portfolioUpdate", {
            "userId": userId,
            "gameId": self.gameId,
            "balance": self.userBalances[userId],
            "totalPortfolioValue": totalValue,
            "positions": self.userPositions.get(userId, {})
        }, room=self.gameId)