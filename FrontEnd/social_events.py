from flask_socketio import SocketIO, join_room, emit
from flask import session

def social_events(socketio, game_service):

    @socketio.on("friend_request")
    def on_friend_request(data):
        success, error = game_service.send_friend_requeest(session["user_id"], data["friend_id"])
        if not success:
            emit("error", {"error" : error})
            return
        emit("friend_request_received", {"from": session["username"]}, to=data["friend_id"])

    @socketio.on("accept_request")
    def on_accept_request(data):
        success, error = game_service.accept_friend_reqest(session["user_id"], data["friend_id"])
        if not success:
            emit("error", {"error": error})
            return
        emit("friend_request_accepted", {"from": session["username"]}, to=data["friend_id"])

    @socketio.on("reject_request")
    def on_rejest_request(data):
        success, error = game_service.reject_friend_request(session["user_id"], data["friend_id"])
        if not success:
            emit("error", {"error": error})
            return
        emit("friend_request_rejected", {"from": session["username"]}, to=data["friend_id"])