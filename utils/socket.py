# first pip install flask-socketio
# init it
from extension import socketio
from flask import request
from flask_socketio import emit, join_room, leave_room, rooms, disconnect
import json


@socketio.on("connect")
def handle_connect(auth):

    # token = auth.get("auth")
    # if not token:
    #     emit(
    #         "connection_responce",
    #         {"status": "error", "message": "Token missing"},
    #         broadcast=False,
    #     )
    #     disconnect()
    #     return
    #     try:
    #         decode_token = decode_token(token)
    #         user_id = decode_token["sub"]
    emit(
        "connection_response",
        {"status": "success", "message": "Connected"},
        broadcast=False,
    )


# except Exception as e:
#     emit(
#         "connection_responce",
#         {"status": "error", "message": str(e)},
#         broadcast=False,
#     )
#     disconnect()


@socketio.on("join_room")
def handle_join_room(data):
    token = data.get("token")
    room_id = data.get("room_id")
    date = data.get("date")
    print(room_id, "room")
    try:
        room_name = f"{room_id}_{date}"
        join_room(room_name)
    except Exception as e:
        print(str(e))
        disconnect()


@socketio.on("leave_room")
def handle_leave_room(data):
    request_data = json.loads(data)
    room_id = request_data.get("room_id")
    date = request_data.get("date")
    room_name = f"{room_id}_{date}"
    leave_room(room_name)
    print(f"Client left room: {room_name}")
