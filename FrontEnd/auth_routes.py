

from flask import Blueprint, request, jsonify, session
from FrontEnd.auth_decorators import registered_only

auth_blueprint = Blueprint("auth", __name__)

def auth_routes(game_service):

    @auth_blueprint.route("/sign_up", methods = ["POST"])
    def sign_up():
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")
        email = data.get("email", "").strip()

        if not username or not password or not email:
            return 

        success, message = game_service.sign_up(username, password, email)
        if success:
            message, number = _login_user(username, password)
            return jsonify({"message" : message}), number
        
        return jsonify({"error" : message}), 400
    
    @auth_blueprint.route("/login", methods = ["POST"])
    def login():
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        message, number = _login_user(username, password)

        return jsonify({"message" : message}), number
    
    @auth_blueprint.route("/log_out", methods = ["POST"])
    def log_out():
        game_service.log_out(session["user_id"], session.get("guest"))
        session.clear()
        return jsonify({"message" : "Logged Out"}),200
    
    @auth_blueprint.route("/guest", methods = ["POST"])
    def guest_login():
        success, user = game_service.create_guest()
        if not success:
            return jsonify({"message" : user}), 400
        session["guest"] = True
        session["username"] = user["username"]
        session["user_id"] = user["user_id"]
        return jsonify({"message" : "Guest Account Created"}), 200
    
    @auth_blueprint.route("/change_password", methods = ["POST"])
    @registered_only
    def change_password():
        data = request.get_json()

        result, error = game_service.change_password(session["user_id"], data["old_password"], data["new_password"])
        if result:
            return jsonify({"message" : "Changed Password"}), 200
        return jsonify({"message" : error}), 401
    
    @auth_blueprint.route("/change_username", methods = ["POST"])
    @registered_only
    def change_username():
        data = request.get_json()

        result, error = game_service.change_username(data["user_id"], data["new_username"])

        if result:
            session["username"] = data["new_username"]
            return jsonify({"message" : "Username Changed"}), 200
        return jsonify({"message" : error}), 401
    
    @auth_blueprint.route("/delete_account", methods = ["POST"])
    @registered_only
    def delete_account():
        result, error = game_service.delete_account(session["user_id"])
        if result:
            session.clear()
            return jsonify({"message" : "Account Deleted"}), 200
        return jsonify({"message" : error}), 401
    

    def _login_user(username, password):
        user, error = game_service.log_in("username", "password")

        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session.pop("guest", None)
            return ("Logged In", 200)
        return (error, 401)
        