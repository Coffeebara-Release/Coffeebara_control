"""
from flask import Flask
from flask_socketio import SocketIO
"""

"""
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def start_server(state_machine):
    @socketio.on("connect")
    def handle_connect():
        print("Client connected")

    @socketio.on("cup update")
    def update_cup(data):
        print("Cup detected:", data)
        socketio.emit("cup update", data)

    @socketio.on("state update")
    def update_state(data):
        print("Device state:", data)
        socketio.emit("state update", data)

    socketio.run(app, host="0.0.0.0", port=8080, debug=False)
"""