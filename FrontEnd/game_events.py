from flask_socketio import SocketIO, join_room, emit
from socket_decorators import socket_in_game, socket_user_required
from flask import session

def game_events(socketio, game_service):

    @socketio.on("join_game")
    @socket_user_required
    @socket_in_game
    def on_join():
        game_id = session.get("game_id")
        if not game_id:
            emit("error", {"error": "No active game"})
            return

        join_room(str(game_id))
        emit("message", {"message": "Joined Game Room"})

        join_room(str(game_id))
        emit("message", {"message": "Joined Game Room"})

    @socketio.on("get_lobby_players")
    @socket_user_required
    @socket_in_game
    def on_get_lobby_players():
        game_id = session.get("game_id")
        if not game_id:
            emit("error", {"error": "Missing game_id"})
            return

        emit_lobby_players(game_id)

    def emit_lobby_players(game_id):
        success, players = game_service.get_lobby_players(game_id)

        if not success:
            emit("error", {"error": players})
            return

        emit(
            "lobby_players",
            {
                "success": True,
                "game_id": game_id,
                "players": players
            },
            to=str(game_id)
        )

    @socketio.on("apply_move")
    @socket_user_required
    @socket_in_game
    def on_move(data):

        move = {
            "move_type" : data["move_type"],
            "user_id" : session["user_id"],
            "card" : data.get("card"),
            "cards" : data.get("cards"),
            "meld_index" : data.get("meld_index")
        }

        success, error = game_service.apply_move(session["game_id"], move)

        if not success:
            emit("error", {"success" : False,
                           "error" : error})
            return
        
        emit_game_state()
        
    @socketio.on("resume_game")
    @socket_user_required
    @socket_in_game
    def on_resume_game():
        success, message = game_service.resume_game(session["game_id"])
        if success:
            emit("message", {"message" : message})
            emit_game_state()
            return
        emit("error", {"error" : message})
        return
    
    def emit_game_state():
        state = game_service.get_game_state(session["game_id"], session["user_id"])
        emit ("game_state", {"success" : True, "state" : state}, to=str(session["game_id"]), include_self= True)