from flask import Blueprint, request, jsonify, session
from FrontEnd.auth_decorators import registered_only, user_required


auth_blueprint = Blueprint("auth", __name__)


def auth_routes(game_service):
    """
    Register all authentication-related routes.

    These routes handle:
    - sign up
    - log in
    - log out
    - guest account creation
    - changing account details
    - deleting an account
    """

    @auth_blueprint.route("/sign_up", methods=["POST"])
    def sign_up():
        """
        Create a new registered user account and log the user in immediately.
        """
        data = request.get_json() or {}

        username = data.get("username", "").strip()
        password = data.get("password", "")
        email = data.get("email", "").strip()

        if not username or not password or not email:
            return jsonify({"error": "Username, password, and email are required"}), 400

        success, message = game_service.sign_up(username, password, email)
        if success:
            message, status_code = _login_user(username, password)
            if status_code >= 400:
                return jsonify({"error": message}), status_code
            return jsonify({"message": message}), status_code

        return jsonify({"error": message}), 400

    @auth_blueprint.route("/login", methods=["POST"])
    def login():
        """
        Log a registered user into an existing account.
        """
        data = request.get_json() or {}

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        message, status_code = _login_user(username, password)
        if status_code >= 400:
            return jsonify({"error": message}), status_code

        return jsonify({"message": message}), status_code

    @auth_blueprint.route("/log_out", methods=["POST"])
    @user_required
    def log_out():
        """
        Log the current user out and clear their session.
        """
        user_id = session.get("user_id")
        guest = session.get("guest", False)

        game_service.log_out(user_id, guest)
        session.clear()

        return jsonify({"message": "Logged Out"}), 200

    @auth_blueprint.route("/guest", methods=["POST"])
    def guest_login():
        """
        Create and log in a guest account.

        If a session already exists, the existing session details are returned.
        """
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

        session["user_id"] = user["user_id"]
        session["username"] = user["username"]
        session["guest"] = True

        return jsonify({
            "message": "Guest Account Created",
            "user_id": user["user_id"],
            "username": user["username"],
            "guest": True
        }), 200

    @auth_blueprint.route("/change_password", methods=["POST"])
    @registered_only
    def change_password():
        """
        Change the password of the currently logged-in registered user.
        """
        data = request.get_json() or {}

        user_id = session.get("user_id")
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not old_password or not new_password:
            return jsonify({"error": "Old password and new password are required"}), 400

        success, error = game_service.change_password(user_id, old_password, new_password)
        if success:
            return jsonify({"message": "Changed Password"}), 200

        return jsonify({"error": error}), 400

    @auth_blueprint.route("/change_username", methods=["POST"])
    @registered_only
    def change_username():
        """
        Change the username of the currently logged-in registered user.
        """
        data = request.get_json() or {}

        user_id = session.get("user_id")
        new_username = data.get("new_username", "").strip()

        if not new_username:
            return jsonify({"error": "New username is required"}), 400

        success, error = game_service.change_username(user_id, new_username)
        if success:
            session["username"] = new_username
            return jsonify({"message": "Username Changed"}), 200

        return jsonify({"error": error}), 400

    @auth_blueprint.route("/delete_account", methods=["POST"])
    @registered_only
    def delete_account():
        """
        Delete the currently logged-in registered user's account.
        """
        success, error = game_service.delete_account(session["user_id"])
        if success:
            session.clear()
            return jsonify({"message": "Account Deleted"}), 200

        return jsonify({"error": error}), 400

    def _login_user(username, password):
        """
        Authenticate a user and store their details in the session.

        Args:
            username (str): The username entered by the user.
            password (str): The password entered by the user.

        Returns:
            tuple: A message and HTTP status code.
        """
        success, user = game_service.log_in(username, password)

        if success:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["guest"] = False
            return "Logged In", 200

        return user, 401