from flask_socketio import SocketIO, join_room, emit
from flask import session

def game_events(socketio, game_service):

    @socketio.on("join_game")
    def on_join():
        join_room(session["game_id"])
        emit("message", {"message" : "Joined Game Room"})
        return

    @socketio.on("apply_move")
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
    def resume_gaon_resume()
        success, message = game_service.resume_game(session["game_id"])
        if success:
            emit("message", {"message" : message})
            emit_game_state()
            return
        emit("error", {"error" : message})
        return
    
    def emit_game_state():
        state = game_service.get_game_state(session["game_id"], session["user_id"])
        emit ("game_state", {"success" : True, "state" : state}, to=session["game_id"], include_self= True)
        
        
