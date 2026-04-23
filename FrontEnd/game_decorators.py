from flask import jsonify, session
from functools import wraps


def in_game(f):
    """
    Restrict access to users who are currently in a game.

    This decorator checks whether a game_id exists in the session.
    If not, the request is rejected.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("game_id"):
            return jsonify({"error": "Not In A Game"}), 403

        return f(*args, **kwargs)

    return wrapper


def not_in_game(f):
    """
    Restrict access to users who are not currently in a game.

    This decorator ensures the user does not already have a game_id
    stored in their session.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("game_id"):
            return jsonify({"error": "Already In A Game"}), 403

        return f(*args, **kwargs)

    return wrapper