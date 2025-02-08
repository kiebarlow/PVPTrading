from solathon import Client, PublicKey, Transaction, Keypair
from solathon.core.instructions import transfer



HOUSEPUBLICWALLET = '41soa6GNXQ3kWSBKVZoZukPGHUvq7bocc7hx7BYVs6xd'
HOUSEPRIVATEWALLET = [168,126,62,125,200,37,57,36,124,119,246,127,109,120,68,48,105,142,228,143,174,93,101,151,233,226,78,177,209,249,106,79,44,204,128,252,24,35,255,198,122,133,143,175,243,193,234,174,162,74,77,109,60,65,130,65,110,50,25,138,144,80,122,190]

client = Client("https://api.devnet.solana.com")
lampartsPerSol = 1000000000
class SolanaStuff:
    def __init__(self, privateKey=None, publicKey=None):
        self.privateKey = privateKey
        self.publicKey = publicKey
        
    def createUserWallet(self)->bool:
        try:
            keypair = Keypair()
            self.privateKey = str(keypair.private_key)
            self.publicKey = str(keypair.public_key)
            return True
        except Exception as e:
            print(str(e))
            return False
        
    def withdrawBalance(self, withdrawAmount, withdrawPublicKey) -> bool:
        """Withdraw amount is in GEMS not SOLANA
        """
        try:
            withdrawAmount = float(withdrawAmount)

            gemsToSol = withdrawAmount / 1000
            
            if gemsToSol != None:
                receiver = withdrawPublicKey
                instruction = transfer(
                    from_public_key=HOUSEPUBLICWALLET,
                    to_public_key=receiver, 
                    lamports=int(((gemsToSol) - 0.02 ) * lampartsPerSol)
                    )
                
                transaction = Transaction(instructions=[instruction], signers=[Keypair.from_private_key(HOUSEPRIVATEWALLET)])
                client.send_transaction(transaction)
                print(transaction)
                return True
            return False
            
        except Exception as e:
            print(str(e))
            return False
        
    def checkForDeposit(self, publicKey, privateKey):
        userEscrowBalance = client.get_balance(publicKey)
        if userEscrowBalance / lampartsPerSol > 0.05:
            receiver = PublicKey(HOUSEPUBLICWALLET)
            instruction = transfer(
                        from_public_key=publicKey,
                        to_public_key=receiver, 
                        lamports=int(((userEscrowBalance / lampartsPerSol) - 0.04 ) * lampartsPerSol)
                    )
            transaction = Transaction(instructions=[instruction], signers=[privateKey])
            client.send_transaction(transaction)
            balanceDeposited = ((userEscrowBalance / lampartsPerSol) - 0.04) * 1000
            return balanceDeposited
        else:
            return 0
          
test = SolanaStuff()

print(test.createUserWallet())

#print(test.withdrawBalance(500, "HmBFrRTd8s1XSm4kqQdKXPtZvmXrohbeS2AW1K7hHdLb"))