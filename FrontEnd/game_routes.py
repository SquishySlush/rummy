from flask import Blueprint, request, jsonify, session
from FrontEnd.auth_decorators import user_required
from FrontEnd.game_decorators import in_game, not_in_game


game_blueprint = Blueprint("game", __name__)


def game_routes(game_service, socketio):
    """
    Register all HTTP routes related to game management.

    These routes handle:
    - creating a game
    - joining a game
    - starting a game
    - pausing a game
    - ending a game
    - loading a paused game
    - rejoining a paused game
    """

    @game_blueprint.route("/create_game", methods=["POST"])
    @user_required
    @not_in_game
    def create_game():
        """
        Create a new game and store its ID in the current session.
        """
        data = request.get_json() or {}

        ruleset = data.get("ruleset")
        seed = data.get("seed")

        if ruleset is None:
            return jsonify({"error": "Ruleset Is Required"}), 400

        game_id, error = game_service.create_game(session["user_id"], ruleset, seed)

        if game_id:
            session["game_id"] = game_id
            return jsonify({"game_id": game_id}), 200

        return jsonify({"error": error}), 400

    @game_blueprint.route("/join_game", methods=["POST"])
    @user_required
    @not_in_game
    def join_game():
        """
        Add the current user to an existing game and store the game ID in session.
        """
        data = request.get_json() or {}

        game_id = data.get("game_id")
        if game_id is None:
            return jsonify({"error": "Game ID Is Required"}), 400

        success, result = game_service.add_player(game_id, session["user_id"])

        if success:
            session["game_id"] = result
            return jsonify({"game_id": result}), 200

        return jsonify({"error": result}), 400

    @game_blueprint.route("/start_game", methods=["POST"])
    @user_required
    @in_game
    def start_game():
        """
        Start the current game and notify all connected players.
        """
        data = request.get_json() or {}
        ruleset = data.get("ruleset")

        if ruleset is None:
            return jsonify({"error": "Ruleset Is Required"}), 400

        success, error = game_service.start_game(session["game_id"], ruleset)

        if not success:
            return jsonify({"error": error}), 400

        socketio.emit(
            "game_started",
            {"game_id": session["game_id"]},
            to=str(session["game_id"])
        )

        return jsonify({"message": "Game Started"}), 200

    @game_blueprint.route("/pause_game", methods=["POST"])
    @user_required
    @in_game
    def pause_game():
        """
        Pause the current game and remove the game ID from session.
        """
        success, error = game_service.pause_game(session["game_id"])
        if not success:
            return jsonify({"error": error}), 400

        session.pop("game_id", None)
        return jsonify({"message": "Game Paused"}), 200

    @game_blueprint.route("/end_game", methods=["POST"])
    @user_required
    @in_game
    def end_game():
        """
        End the current game and remove the game ID from session.
        """
        success, result = game_service.end_game(session["game_id"])
        if not success:
            return jsonify({"error": result}), 400

        session.pop("game_id", None)
        return jsonify({"message": "Game Ended", "results": result}), 200

    @game_blueprint.route("/load_paused_game", methods=["POST"])
    @user_required
    @not_in_game
    def load_paused_game():
        """
        Load a paused game back into memory and store its ID in session.
        """
        data = request.get_json() or {}

        game_id = data.get("game_id")
        if game_id is None:
            return jsonify({"error": "Game ID Is Required"}), 400

        success, message = game_service.load_paused_game(game_id, session["user_id"])
        if not success:
            return jsonify({"error": message}), 400

        session["game_id"] = game_id
        return jsonify({"message": message}), 200

    @game_blueprint.route("/rejoin_game", methods=["POST"])
    @user_required
    @not_in_game
    def rejoin_game():
        """
        Rejoin an existing paused or active game and store its ID in session.
        """
        data = request.get_json() or {}

        game_id = data.get("game_id")
        if game_id is None:
            return jsonify({"error": "Game ID Is Required"}), 400

        success, error = game_service.rejoin_game(game_id, session["user_id"])
        if not success:
            return jsonify({"error": error}), 400

        session["game_id"] = game_id
        return jsonify({"message": "Joined Game"}), 200