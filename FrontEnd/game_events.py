from flask_socketio import join_room, emit
from .socket_decorators import socket_in_game, socket_user_required
from flask import session


def game_events(socketio, game_service):
    """
    Register all Socket.IO event handlers related to game activity.

    These events handle:
    - joining a game room
    - retrieving lobby players
    - applying moves
    - pausing a game on disconnect
    - resuming a paused game
    - sending updated game state to clients
    """

    @socketio.on("join_game")
    @socket_user_required
    @socket_in_game
    def on_join():
        """
        Add the current user to the Socket.IO room for their active game.
        """
        game_id = session.get("game_id")
        if not game_id:
            emit("error", {"error": "No Active Game"})
            return

        join_room(str(game_id))
        emit("message", {"message": "Joined Game Room"})

    @socketio.on("get_lobby_players")
    @socket_user_required
    @socket_in_game
    def on_get_lobby_players():
        """
        Send the current lobby player list to everyone in the game room.
        """
        game_id = session.get("game_id")
        if not game_id:
            emit("error", {"error": "Missing Game ID"})
            return

        emit_lobby_players(game_id)

    def emit_lobby_players(game_id):
        """
        Retrieve the list of players in the lobby and emit it to the game room.

        Args:
            game_id: The ID of the game whose lobby players should be sent.
        """
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
        """
        Apply a move made by the current player and then emit the updated game state.
        """
        move = {
            "move_type": data["move_type"],
            "user_id": session["user_id"],
            "card": data.get("card"),
            "cards": data.get("cards"),
            "meld_index": data.get("meld_index")
        }

        success, error = game_service.apply_move(session["game_id"], move)

        if not success:
            emit("error", {"success": False, "error": error})
            return

        emit_game_state()

    @socketio.on("disconnect")
    def on_disconnect():
        """
        Pause the current game if a user disconnects while in an active game.
        """
        user_id = session.get("user_id")
        game_id = session.get("game_id")

        if not user_id or not game_id:
            return

        success, message = game_service.pause_game(game_id)
        if not success:
            return

        session.pop("game_id", None)

        emit(
            "game_paused",
            {
                "message": "A Player Disconnected. The Game Was Paused."
            },
            to=str(game_id)
        )

    @socketio.on("resume_game")
    @socket_user_required
    @socket_in_game
    def on_resume_game():
        """
        Resume a paused game and emit the refreshed game state.
        """
        success, message = game_service.resume_game(session["game_id"])

        if success:
            emit("message", {"message": message})
            emit_game_state()
            return

        emit("error", {"error": message})

    def emit_game_state():
        """
        Retrieve the latest game state for the current session user
        and emit it to all players in the game room.
        """
        success, state = game_service.get_game_state(session["game_id"], session["user_id"])

        if not success:
            emit("error", {"error": state})
            return

        emit(
            "game_state",
            {"success": True, "state": state},
            to=str(session["game_id"]),
            include_self=True
        )