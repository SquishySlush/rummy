from flask_socketio import SocketIO, join_room, emit
from .socket_decorators import socket_user_required, socket_registered_only

from flask import session

def social_events(socketio, game_service):

    @socketio.on("connect")
    def on_connect():
        user_id = session.get("user_id")
        if user_id is not None:
            join_room(f"user_{user_id}")

    @socketio.on("friend_request")
    @socket_registered_only
    def on_friend_request(data):
        success, error = game_service.send_friend_request(session["user_id"], data["friend_id"])
        if not success:
            emit("error", {"error" : error})
            return
        emit("friend_request_received", {"from_id": session["user_id"], "from_username": session["username"]}, to=f"user_{data['friend_id']}")

    @socketio.on("accept_request")
    @socket_registered_only
    def on_accept_request(data):
        success, error = game_service.accept_friend_request(session["user_id"], data["friend_id"])
        if not success:
            emit("error", {"error": error})
            return
        emit("friend_request_accepted", {"from_id": session["user_id"], "from_username": session["username"]}, to=f"user_{data['friend_id']}")

    @socketio.on("reject_request")
    @socket_registered_only
    def on_rejest_request(data):
        success, error = game_service.reject_friend_request(session["user_id"], data["friend_id"])
        if not success:
            emit("error", {"error": error})
            return
        emit("friend_request_rejected", {"from_id": session["user_id"], "from_username": session["username"]}, to=f"user_{data['friend_id']}")

    @socketio.on("get_socials")
    @socket_registered_only
    def on_get_socials():
        user_id = session.get("user_id")
        
        if user_id is None:
            emit("error", {"error": "Missing User Id"})
        
        success, friends = game_service.get_friends(user_id)
        if not success:
            friends = []
        
        success, pending = game_service.get_pending_requests(user_id)
        if not success:
            pending = []
        
        success, others = game_service.get_all_users_except(user_id)
        if not success:
            others = []
        
        emit("social_list",
             {
                 "success": True,
                 "friends": friends,
                 "pending": pending,
                 "others": others
             })
        
    
    @socketio.on("get_history")
    @socket_registered_only
    def on_get_history():
        user_id = session.get("user_id")

        success, history = game_service.get_player_history(user_id)
        if not success:
            emit("game_history", {"success": False, "history": [], "error": history})
            return

        emit("game_history", {"success": True, "history": history})

    @socketio.on("invite_to_lobby")
    @socket_registered_only
    def on_invite_to_lobby(data):
        user_id = session.get("user_id")
        username = session.get("username")
        friend_id = data.get("friend_id")
        game_id = session.get("game_id")

        if not user_id or not friend_id or not game_id:
            emit("error", {"error": "Missing data"})
            return

        success, error = game_service.send_lobby_invite(user_id, friend_id, game_id)
        if not success:
            emit("error", {"error": error})
            return

        emit(
            "lobby_invite_received",
            {
                "from_id": user_id,
                "from_username": username,
                "game_id": game_id
            },
            to=f"user_{friend_id}"
        )
    @socketio.on("accept_lobby_invite")
    @socket_user_required
    def on_accept_lobby_invite(data):
        user_id = session.get("user_id")
        game_id = data.get("game_id")

        if not user_id or not game_id:
            emit("error", {"error": "Missing data"})
            return

        game_service.add_player_to_game(user_id, game_id, "Player")

        emit(
            "lobby_joined",
            {"game_id": game_id},
        )

    @socketio.on("ready")
    @socket_user_required
    def on_ready(data):
        user_id = session.get("user_id")
        game_id = data.get("game_id")
        success, error = game_service.ready(user_id, game_id)
        if not success:
            emit("error", {"error": error})
            return
        emit("message", {"message": "Readied Up"})
        return
        
        