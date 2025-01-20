from app import app
from extension import socketio
from utils import handle_connect, handle_leave_room, handle_join_room
if __name__ == "__main__":
    socketio.run(app, port=5000, host="0.0.0.0")