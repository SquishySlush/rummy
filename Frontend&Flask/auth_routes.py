

from flask import Blueprint, request, jsonify, session
from auth_decorators import registered_only

auth_blueprint = Blueprint("auth", __name__)

def auth_routes(game_service):

    @auth_blueprint.route("/sign_up", methods = ["POST"])
    def sign_up():
        data = request.get_json()

        success, message = game_service.sign_up(data["username"], data["password"])
        if success:
            return jsonify({"message" : message}), 201
        return jsonify({"error" : message}), 400
    
    @auth_blueprint.route("/login", methods = ["POST"])
    def login():
        data = request.get_json()

        user, error = game_service.log_in(data["username"], data{"password"})
        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            return jsonify({"message" : "Logged In"}), 200
        
        return jsonify({"error" : error}), 401
    
    @auth_blueprint.route("/log_out", methods = ["POST"])
    @registered_only
    def log_out():
        game_service.log_out(session["user_id"], session.get("guest"))
        session.clear()
        return jsonify({"message" : "Logged Out"}),200
    
    @auth_blueprint.route("/guest", methods = ["POST"])
    def guest_login():
        game_service.create_guest()
        session["guest"] = True
        session["username"] = "Guest"
        return jsonify({"mssage" : "Guest Account Created"}), 200
    
    @auth_blueprint.route("/change_password", methods = ["POST"])
    @registered_only
    def change_password():
        data = request.get_json()

        result, error = game_service.change_password(data["user_id"], data["old_password"], data["new_password"])
        if result:
            return jsonify({"message" : "Changed Password"}), 200
        return jsonify({"message" : error}), 401
    
    @auth_blueprint.route("/change_username", methods = ["POST"])
    @registered_only
    def change_username():
        data = request.get_json()

        result, error = game_service.change_username(data["user_id"], data["new_username"])

        if result:
            return jsonify({"message" : "Username Changed"}), 200
        return jsonify({"message" : error}), 401
    
    @auth_blueprint.route("/delete_account", methods = ["POST"])
    @registered_only
    def delete_account():
        data = request.get_json()

        result, error = game_service.delete_account(data["user_id"])
        if result:
            return jsonify({"message" : "Account Deleted"}), 200
        return jsonify({"message" : error}), 401