from functools import wraps
from flask import session
from flask_socketio import emit

def socket_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            emit("error", {"error": "Login Required"})
            return
        return f(*args, **kwargs)
    return wrapper


def socket_registered_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            emit("error", {"error": "Login Required"})
            return
        if session.get("guest", False):
            emit("error", {"error" : "Registered Account Required"})
            return
        return f(*args, **kwargs)
    return wrapper

def socket_in_game(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("game_id"):
            emit("error", {"error": "Not In a Game"})
            return
        return f(*args, **kwargs)
    return wrapper
