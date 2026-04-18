from flask import Blueprint, request, jsonify, session
from FrontEnd.auth_decorators import registered_only, user_required

auth_blueprint = Blueprint("auth", __name__)

def auth_routes(game_service):

    @auth_blueprint.route("/sign_up", methods = ["POST"])
    def sign_up():
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")
        email = data.get("email", "").strip()

        if not username or not password or not email:
            return jsonify({"error": "Username, password, and email are required"}), 400

        success, message = game_service.sign_up(username, password, email)
        if success:
            message, number = _login_user(username, password)
            if number >= 400:
                return jsonify({"error": message}), number
            return jsonify({"message" : message}), number

        return jsonify({"error" : message}), 400

    @auth_blueprint.route("/login", methods = ["POST"])
    def login():
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        message, number = _login_user(username, password)
        if number >= 400:
            return jsonify({"error": message}), number
        return jsonify({"message" : message}), number

    @auth_blueprint.route("/log_out", methods = ["POST"])
    @user_required
    def log_out():
        user_id = session.get("user_id")
        guest = session.get("guest", None)

        game_service.log_out(user_id, guest)
        session.clear()
        return jsonify({"message" : "Logged Out"}), 200

    @auth_blueprint.route("/guest", methods=["POST"])
    def guest_login():
        if session.get("user_id"):
            return jsonify({
                "message": "Session already exists",
                "user_id": session["user_id"],
                "username": session.get("username"),
                "guest": session.get("guest", False)
            }), 200

        success, user = game_service.create_guest()
        if not success:
            return jsonify({"error": user}), 400

        session["guest"] = True
        session["username"] = user["username"]
        session["user_id"] = user["user_id"]

        return jsonify({
            "message": "Guest account created",
            "user_id": user["user_id"],
            "username": user["username"],
            "guest": True
        }), 200

    @auth_blueprint.route("/change_password", methods = ["POST"])
    @registered_only
    def change_password():
        data = request.get_json()
        user_id = session.get("user_id")
        old_password = data.get("old_password", None)
        new_password = data.get("new_password", None)

        result, error = game_service.change_password(user_id, old_password, new_password)
        if result:
            return jsonify({"message" : "Changed Password"}), 200
        return jsonify({"error" : error}), 400

    @auth_blueprint.route("/change_username", methods = ["POST"])
    @registered_only
    def change_username():
        data = request.get_json()
        user_id = session.get("user_id")
        new_username = data.get("new_username", None)

        result, error = game_service.change_username(user_id, new_username)

        if result:
            session["username"] = data["new_username"]
            return jsonify({"message" : "Username Changed"}), 200
        return jsonify({"error" : error}), 400

    @auth_blueprint.route("/delete_account", methods = ["POST"])
    @registered_only
    def delete_account():
        result, error = game_service.delete_account(session["user_id"])
        if result:
            session.clear()
            return jsonify({"message" : "Account Deleted"}), 200
        return jsonify({"error" : error}), 400


    def _login_user(username, password):
        success, user = game_service.log_in(username, password)

        if success:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["guest"] = False
            session.pop("guest", None)
            return ("Logged In", 200)
        return (user, 401)
