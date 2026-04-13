
from flask import Blueprint, request, jsonify, session
from auth_decorators import registered_only

game_blueprint = Blueprint("game", __name__)

def game_routes(game_service):

    @auth_blueprint.route("/create_game", methods = ["POST"])
    @registered_only
    def create_game():
        data = request.get_json()
        
