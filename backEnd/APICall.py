from solanaStuff import SolanaStuff
from Database import *

def DepositGems(usrName):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT WalletID FROM User WHERE UserName = ?", (usrName))
    wallID = cursor.fetchall()
    cursor.execute("SELECT * FROM Wallet WHERE WalletID = ?",(wallID))
    wallInfo = cursor.fetchall()
    depo = SolanaStuff.checkForDeposit(wallInfo[1], wallInfo[2])
    addGems(usrName,depo)
    conn.close()
    numGems = checkNumOfGems(usrName)
    return numGems
    """Now add a retrieve number of gems.
    """
    
def WithdrawSol(usrName, solAdress, numOfGems):
    numGems = checkNumOfGems(usrName)
    if numGems<numOfGems:
        return False
    elif SolanaStuff.withdrawBalance(numOfGems,solAdress):
        withdrawGems(usrName,numOfGems)
        return True
    else:
        return False
    """Return true or false
    """
    
    
def siteLogin(usrName, passwd):
    user = checkUser(usrName,passwd)
    if user != 0:
        return True
    else:
        return False
    """Return true if the user login is successful.
    """
    
def siteRegister(usrName, passwd):
    available =  checkUser(usrName,passwd)
    if available == 0:
        wallID = createUser(usrName,passwd)
        user = SolanaStuff()
        user.createUserWallet()
        pub = user.publicKey
        priv = user.privateKey
        createWallet(wallID,pub,priv)
        return True
    else:
        return False
    """Return true if the creation of a user is successful.
    """