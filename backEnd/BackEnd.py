from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
import time
import threading
import DataHandler, Database, solanaStuff

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jrhbieygfhcbvhwruygv32rughf123ttrplace1beuygfreoubvwro'
socketio = SocketIO(app, ping_timeout=5, ping_interval=15, logger=True, engineio_logger=True)

# Initialize the data handler
dataHandler = DataHandler.BinanceDataHandler(socketio)

lobbies = {}
LOBBY_TIMER_DURATION = 60

def startLobbyTimer(lobbyId):
    def timerThread():
        remaining = LOBBY_TIMER_DURATION
        while remaining > 0:
            # Emit the current timer value to all clients in the lobby
            socketio.emit('lobbyTimer', {'lobbyId': lobbyId, 'timeRemaining': remaining})
            time.sleep(1)
            remaining -= 1
        # Timer finished—broadcast that the game is starting!
        socketio.emit('gameStart', {'lobbyId': lobbyId}, room=lobbyId)
    threading.Thread(target=timerThread).start()

@app.route("/")
def helloWorld():
    return "<p>Hello World!</p>"

@socketio.on('connect')
def onConnect():
    emit('lobby_list', lobbies)
    
@socketio.on('createLobby')
def handleCreateLobby(data):
    """
    Expected data: {
      'lobbyId': unique identifier,
      'lobbyName': display name,
      'minCoins': minimum coins required to join (e.g., 50),
      'userId': the user's name,
      'coins': the number of coins the user has
    }
    """
    lobbyId = data.get('lobbyId')
    lobbyName = data.get('lobbyName')
    minCoins = data.get('minCoins', 0)
    userId = data.get('userId')
    userCoins = data.get('coins', 0)
    
    # Check coin requirement.
    if userCoins < minCoins:
        emit('error', {'msg': 'Not enough coins to create this lobby.'})
        return
    # Check if the user is already in a lobby
    for lobby in lobbies.values():
        if userId in lobby['players']:
            emit('error', {'msg': 'User already in a lobby.'})
            return
    
    if lobbyId and lobbyId not in lobbies:
        lobbies[lobbyId] = {
            'name': lobbyName,
            'players': [],
            'min_coins': minCoins,
        }
        # Broadcast updated lobby list to all connected clients.
        emit('lobbyList', lobbies, broadcast=True)
        startLobbyTimer(lobbyId)
    else:
        emit('error', {'msg': 'Invalid lobby id or lobby already exists.'})
        
@socketio.on('joinLobby')
def handleJoinLobby(data):
    """
    Expected data: {
      'lobbyId': the lobby the user wants to join,
      'userId': the user's name,
      'coins': the number of coins the user has
    }
    """
    lobbyId = data.get('lobbyId')
    userId = data.get('userId')
    userCoins = data.get('coins', 0)
    
    if lobbyId not in lobbies:
        emit('error', {'msg': 'Lobby not found.'})
        return

    lobby = lobbies[lobbyId]
    required = lobby.get('minCoins', 0)
    
    # Check coin requirement.
    if userCoins < required:
        emit('error', {'msg': 'Not enough coins to join this lobby.'})
        return
    # Check if the user is already in a lobby
    for lobby in lobbies.values():
        if userId in lobby['players']:
            emit('error', {'msg': 'User already in a lobby.'})
            return

    # Add user to the lobby.
    lobby['players'].append(userId)
    join_room(lobbyId)
    
    # Broadcast the updated lobby list to all clients.
    emit('lobbyList', lobbies, broadcast=True)
    
@socketio.on('leaveLobby')
def handleLeaveLobby(data):
    """
    Expected data: {
      'lobbyId': the lobby the user wants to leave,
      'userId': the user's name
    }
    """
    lobbyId = data.get('lobbyId')
    userId = data.get('userId')
    
    if lobbyId not in lobbies:
        emit('error', {'msg': 'Lobby not found.'})
        return

    lobby = lobbies[lobbyId]
    if userId in lobby['players']:
        lobby['players'].remove(userId)
        leave_room(lobbyId)
        if not lobby['players']:
            del lobbies[lobbyId]
            close_room(lobbyId)
        
        # Broadcast the updated lobby list to all clients.
        emit('lobbyList', lobbies, broadcast=True)
    else:
        emit('error', {'msg': 'User not found in lobby.'})
        
@socketio.on('disconnect')
def handleDisconnect():
    print('Client disconnected')
    for lobbyId, lobby in lobbies.items():
        if request.sid in lobby['players']:
            lobby['players'].remove(request.sid)
            leave_room(lobbyId)
            if not lobby['players']:
                del lobbies[lobbyId]
                close_room(lobbyId)
            emit('lobbyList', lobbies, broadcast=True)
            break      
        
@socketio.on('historicalData')
def handleHistoricalData(data):
    ticker = str(data).upper()
    timeframe = 10
    # Get historical data for the specified ticker and timeframe.
    historicalData = dataHandler.getCachedKlines(ticker, timeframe)
    emit('historicalData', historicalData)
        
if __name__ == "__main__":
    socketio.run(app, debug=True)