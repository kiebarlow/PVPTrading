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
    
# Create a new lobby.
@socketio.on('create_lobby')
def create_lobby(data):
    # data should include a unique lobby id and lobby name
    lobby_id = data.get('lobby_id')
    lobby_name = data.get('lobby_name')
    if lobby_id and lobby_id not in lobbies:
        lobbies[lobby_id] = {'name': lobby_name, 'players': []}
        # Broadcast the updated lobby list to all connected clients.
        emit('lobby_list', lobbies, broadcast=True)
    else:
        emit('error', {'msg': 'Lobby already exists or invalid lobby id.'})
        
# Player joins a lobby.
@socketio.on('join_lobby')
def join_lobby(data):
    lobby_id = data.get('lobby_id')
    username = data.get('username')
    if lobby_id in lobbies:
        lobbies[lobby_id]['players'].append(username)
        # Optionally, add the client to a SocketIO "room"
        join_room(lobby_id)
        # Broadcast update for that lobby (or send the whole lobby list)
        emit('lobby_list', lobbies, broadcast=True)
    else:
        emit('error', {'msg': 'Lobby not found.'})