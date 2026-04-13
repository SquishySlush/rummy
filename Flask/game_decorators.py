
from flask import jsonify, session
from functools import wraps

def in_game(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("game_id"):
            return jsonify({"message" : "Not In A Game"}), 403
        return f(*args, **kwargs)
    return wrapper

def not_in_game(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("game_id"):
            return jsonify({"message" : "In A Game"}), 403
        return f(*args, **kwargs)
    return wrapper