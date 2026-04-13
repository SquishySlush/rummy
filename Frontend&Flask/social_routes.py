from flask import Blueprint, request, jsonify, session
from auth_decorators import registered_only

social_blueprint = Blueprint("social", __name__)

def social_routes(game_service):

    @social_blueprint.route("/friends", methods = ["GET"])
    @registered_only
    def get_friends():
        success, data = game_service.get_friends(session["user_id"])
        if success:
            return jsonify({"friends": data}), 200
        return jsonify({"error": data}), 400
    
    @social_blueprint.route("/pending_requests", methods = ["GET"])
    @registered_only
    def get_requests():
        success, data = game_service.get_pending_requests(session["user_id"])
        if success:
            return jsonify({"requests": data}), 200
        return jsonify({"error": data}), 400
    
    @social_blueprint.route("/history", methods = ["GET"])
    @registered_only
    def get_player_history():
        success, data = game_service.get_player_history(session["user_id"])
        if success:
            return jsonify({"history": data}), 200
        return jsonify({"error": data}), 400