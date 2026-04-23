from flask import jsonify, session
from functools import wraps


def registered_only(f):
    """
    Restrict access to registered users only.

    This decorator checks that:
    - a user is logged in
    - the logged-in account is not a guest account

    If either condition fails, a JSON error response is returned instead
    of allowing the route to continue.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Account Required"}), 401

        if session.get("guest", False):
            return jsonify({"error": "Registered Account Required"}), 403

        return f(*args, **kwargs)

    return wrapper


def user_required(f):
    """
    Restrict access to logged-in users only.

    This decorator checks whether a user ID exists in the session.
    If not, the request is rejected with a JSON error response.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Account Required"}), 401

        return f(*args, **kwargs)

    return wrapper