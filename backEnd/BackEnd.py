from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jrhbieygfhcbvhwruygv32rughf123ttrplace1beuygfreoubvwro'
socketio = SocketIO(app,ping_timeout=5, ping_interval=15, logger=True, engineio_logger=True)

lobbies = {}
LOBBY_TIMER_DURATION = 60

def start_lobby_timer(lobby_id):
    def timer_thread():
        remaining = LOBBY_TIMER_DURATION
        while remaining > 0:
            # Emit the current timer value to all clients in the lobby
            socketio.emit('lobby_timer', {'lobby_id': lobby_id, 'time_remaining': remaining}, room=lobby_id)
            time.sleep(1)
            remaining -= 1
        # Timer finished—broadcast that the game is starting!
        socketio.emit('game_start', {'lobby_id': lobby_id}, room=lobby_id)
    threading.Thread(target=timer_thread).start()

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@socketio.on('connect')
def on_connect():
    emit('lobby_list', lobbies)
    
@socketio.on('create_lobby')
def handle_create_lobby(data):
    """
    Expected data: {
      'lobby_id': unique identifier,
      'lobby_name': display name,
      'min_coins': minimum coins required to join (e.g., 50),
      'user_id': the user's name,
      'coins': the number of coins the user has
    }
    """
    lobby_id = data.get('lobby_id')
    lobby_name = data.get('lobby_name')
    min_coins = data.get('min_coins', 0)
    user_id = data.get('user_id')
    user_coins = data.get('coins',0)
    
    # Check coin requirement.
    if user_coins < min_coins:
        emit('error', {'msg': 'Not enough coins to create this lobby.'})
        return
    # Check if the user is already in a lobby
    for lobby in lobbies.values():
        if user_id in lobby['players']:
            emit('error', {'msg': 'User already in a lobby.'})
            return
    
    if lobby_id and lobby_id not in lobbies:
        lobbies[lobby_id] = {
            'name': lobby_name,
            'players': [],
            'min_coins': min_coins,
        }
        # Broadcast updated lobby list to all connected clients.
        emit('lobby_list', lobbies, broadcast=True)
        start_lobby_timer(lobby_id)
    else:
        emit('error', {'msg': 'Invalid lobby id or lobby already exists.'})
        
@socketio.on('join_lobby')
def handle_join_lobby(data):
    """
    Expected data: {
      'lobby_id': the lobby the user wants to join,
      'user_id': the user's name,
      'coins': the number of coins the user has
    }
    """
    lobby_id = data.get('lobby_id')
    user_id = data.get('user_id')
    user_coins = data.get('coins', 0)
    
    if lobby_id not in lobbies:
        emit('error', {'msg': 'Lobby not found.'})
        return

    lobby = lobbies[lobby_id]
    required = lobby.get('min_coins', 0)
    
    # Check coin requirement.
    if user_coins < required:
        emit('error', {'msg': 'Not enough coins to join this lobby.'})
        return
    # Check if the user is already in a lobby
    for lobby in lobbies.values():
        if user_id in lobby['players']:
            emit('error', {'msg': 'User already in a lobby.'})
            return

    # Add user to the lobby.
    lobby['players'].append(user_id)
    join_room(lobby_id)
    
    # Broadcast the updated lobby list to all clients.
    emit('lobby_list', lobbies, broadcast=True)
    
@socketio.on('leave_lobby')
def handle_leave_lobby(data):
    """
    Expected data: {
      'lobby_id': the lobby the user wants to leave,
      'user_id': the user's name
    }
    """
    lobby_id = data.get('lobby_id')
    user_id = data.get('user_id')
    
    if lobby_id not in lobbies:
        emit('error', {'msg': 'Lobby not found.'})
        return

    lobby = lobbies[lobby_id]
    if user_id in lobby['players']:
        lobby['players'].remove(user_id)
        leave_room(lobby_id)
        if not lobby['players']:
            del lobbies[lobby_id]
            close_room(lobby_id)
        
        # Broadcast the updated lobby list to all clients.
        emit('lobby_list', lobbies, broadcast=True)
    else:
        emit('error', {'msg': 'User not found in lobby.'})
        
# No fucking idea hopefully copilot cooked        
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    for lobby_id, lobby in lobbies.items():
        if request.sid in lobby['players']:
            lobby['players'].remove(request.sid)
            leave_room(lobby_id)
            if not lobby['players']:
                del lobbies[lobby_id]
                close_room(lobby_id)
            emit('lobby_list', lobbies, broadcast=True)
            break      

#handle trade requests  
@socketio.on('trade_open')
def handle_trade_open(data):
    """
    Expected data: {
      'lobby_id': the lobby the trade is happening in,
      'user_id': the user initiating the trade,
      'ticker': the stock ticker being traded,
      'quantity': the number of shares being traded,
      'leverage': the leverage being used (e.g., 1.5x),
      'action': the action being taken (e.g., 'buy' or 'sell')
    }
    """
    lobby_id = data.get('lobby_id')
    user_id = data.get('user_id')
    ticker = data.get('ticker')
    quantity = data.get('quantity')
    leverage = data.get('leverage', 1)
    action = data.get('action')
    timestamp = time.time()
    # check closest timestamp of binance data
    
    
    emit('trade_open', data, room=lobby_id)
        
@socketio.on('trade_close')
def handle_trade_close(data):
    """
    Expected data: {
      'lobby_id': the lobby the trade is happening in,
      'user_id': the user initiating the trade,
      'ticker': the stock ticker being traded,
      'quantity': the number of shares being traded,
      'leverage': the leverage being used (e.g., 1.5x),
      'action': the action being taken (e.g., 'buy' or 'sell')
    }
    """
    lobby_id = data.get('lobby_id')
    user_id = data.get('user_id')
    
        
if __name__ == "__main__":
    socketio.run(app, debug=True)