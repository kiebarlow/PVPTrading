from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jrhbieygfhcbvhwruygv32rughf123ttrplace1beuygfreoubvwro'
socketio = SocketIO(app)

lobbies = {}

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
      'min_coins': minimum coins required to join (e.g., 50)
    }
    """
    lobby_id = data.get('lobby_id')
    lobby_name = data.get('lobby_name')
    min_coins = data.get('min_coins', 0)
    
    if lobby_id and lobby_id not in lobbies:
        lobbies[lobby_id] = {
            'name': lobby_name,
            'players': [],
            'min_coins': min_coins,
        }
        # Broadcast updated lobby list to all connected clients.
        emit('lobby_list', lobbies, broadcast=True)
    else:
        emit('error', {'msg': 'Invalid lobby id or lobby already exists.'})
        
@socketio.on('join_lobby')
def handle_join_lobby(data):
    """
    Expected data: {
      'lobby_id': the lobby the user wants to join,
      'username': the user’s name,
      'coins': the number of coins the user has
    }
    """
    lobby_id = data.get('lobby_id')
    username = data.get('username')
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

    # Add user to the lobby.
    lobby['players'].append(username)
    join_room(lobby_id)
    
    # Broadcast the updated lobby list to all clients.
    emit('lobby_list', lobbies, broadcast=True)