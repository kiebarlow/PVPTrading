import sqlite3
import uuid

# Creates a new user in the database.
def createUser(usrID, usrNm, wallID):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User VALUES (?,?,?,?)", (usrID,usrNm,wallID,0))
    conn.commit()
    conn.close()
    
# Updates the gems balance for a user's account. 
def addGems(usrID,gems):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Gems FROM User WHERE UserID = ?",(usrID))
    balance = cursor.fetchall()
    balance += gems
    cursor.execute("UPDATE User SET Gems = ? WHERE UserID = ?", (balance,usrID))
    conn.commit()
    conn.close()

# Creates a new crypto wallet information instance for a user.
def createWallet(wallID,pubKey,privKey):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Escro VALUES (?,?,?)", (wallID,pubKey,privKey))
    conn.commit()
    conn.close()

# Creates a new instance of a game when a user starts one.
def createGame(start,end,jackpot):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    gameID = uuid.uuid4()
    cursor.execute("INSERT INTO Game VALUES (?,?,?,?,?,?)",(gameID,start,end,jackpot,"Y"))
    conn.commit()
    conn.close()
    return gameID

# Creates a new instance of joining a game.
def joinGame(gameID,usrID):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    gameID = uuid.uuid4()
    cursor.execute("INSERT INTO Game VALUES (?,?)",(gameID,usrID))
    conn.commit()
    conn.close()
    
# Logs a new trade made by a user.
def newTrade(gameID,usrID,amount,time,tradeType,coinTraded,sold,leverage):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Trade VALUES (?,?,?,?,?,?,?,?)",(gameID,usrID,amount,time,tradeType,coinTraded,sold,leverage))
    conn.commit()
    conn.close()
    