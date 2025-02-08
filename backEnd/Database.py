import sqlite3
import uuid

#Creates an instance of the connection
def connect():
    conn = sqlite3.connect('PVPTradingDatabase.db')
    return conn

# Creates a new user in the database.
def createUser(usrNm, passwd):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    usrID = str(uuid.uuid4())
    wallID = str(uuid.uuid4())
    cursor.execute("INSERT INTO User VALUES (?,?,?,?,?)", (usrID,usrNm,wallID,0,passwd))
    conn.commit()
    conn.close()
    return wallID
    
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
    
def withdrawGems(usrID,withdrawal):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Gems FROM User WHERE UserID = ?",(usrID))
    balance = cursor.fetchall()
    balance -= withdrawal
    cursor.execute("UPDATE User SET Gems = ? WHERE UserID = ?", (balance,usrID))
    conn.commit()
    conn.close()
    
def checkNumOfGems(usrID):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Gems FROM User WHERE UserID = ?",(usrID))
    balance = cursor.fetchall()
    conn.close()
    return balance


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

# Update the jackpot total.
def updateJackpot(gameID,input):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Jackpot FROM Game WHERE GameID = ?",(gameID))
    jackpot = cursor.fetchall()
    jackpot += input
    cursor.execute("UPDATE User SET Jackpot = ? WHERE GameID = ?", (jackpot,gameID))
    conn.commit()
    conn.close()
   
# Close the game after it starts. 
def closeGame(gameID):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Game SET Joinable = ? WHERE GameID = ?", ("N",gameID))
    conn.commit()
    conn.close()

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
    
# Get a list of all games that are currently joinable or past.
# Takes string as input for function (Y/N)
def currentGames(decider):
    conn = sqlite3.connect('PVPTradingDatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Game WHERE Joinable = ?",(decider))
    currGames = cursor.fetchall()
    conn.close()
    return currGames

def checkUser(usrName, passwd):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE UserName = ? AND Password = ?",(usrName,passwd))
    user = cursor.fetchall()
    conn.close()
    return user

    