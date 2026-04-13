
from flask import Blueprint, request, jsonify, session
from auth_decorators import registered_only
from game_decorators import in_game, not_in_game

game_blueprint = Blueprint("game", __name__)

def game_routes(game_service):

    @game_blueprint.route("/create_game", methods = ["POST"])
    @registered_only
    @not_in_game
    def create_game():
        data = request.get_json()
        game_id, error = game_service.create_game(session["user_id"], data["ruleset"], data["seed"])

        if game_id:
            session["game_id"] = game_id
            return jsonify({"game_id" : game_id}), 200
        return jsonify({"message" : error})
    
    @game_blueprint.route("/join_game", methods = ["POST"])
    @not_in_game
    def join_game():
        data = request.get_json()
        valid, game_id =  game_service.add_player(session["user_id"], data["game_id"])

        if valid:
            session["game_id"] = game_id
            return jsonify({"game_id" : game_id}), 200
        return jsonify({"Message" : game_id})
    
    @game_blueprint.route("/start_game", methods = ["POST"])
    @in_game
    def start_game():
        game_service.start_game(session["game_id"])
        return jsonify({"game_status" : "Game Started"})

    @game_blueprint.route("/pause_game", methods = ["POST"])
    @in_game
    def pause_game():
        game_service.pause_game(session["game_id"])
        session.pop("game_id")
        return jsonify({"message" : "Game Paused"}), 200

    @game_blueprint.route("/end_game", methods = ["POST"])
    @in_game
    def end_game():
        game_service.end_game(session["game_id"])
        session.pop("game_id")
        return jsonify({"message" : "Game Ended"}), 200
    
    @game_blueprint.route("/load_pause_game", methods = ["POST"])
    @not_in_game
    def load_paused_game():
        data = request.get_json()

        success, message = game_service.load_paused_game(data["game_id"], session["user_id"])
        if not success:
            return jsonify({"message" : message})
        
        session["game_id"] = data["game_id"]
        return jsonify({"message" : message}), 200
    
    @game_blueprint.route("/rejoin_game", methods = ["POST"])
    @not_in_game
    def rejoin_game():
        data = request.get_json()

        success, error, = game_service.rejoin_game(data["game_id"], session["user_id"])
        if not success:
            return jsonify({"message": error}), 401
        
        session["game_id"] = data["game_id"]
        return jsonify({"message" : "Joined Paused Game"}), 200