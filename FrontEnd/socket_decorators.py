from functools import wraps
from flask import session
from flask_socketio import emit


def socket_user_required(f):
    """
    Restrict a Socket.IO event to logged-in users only.

    This decorator checks whether a user ID exists in the session.
    If not, an error event is emitted and the handler is not run.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            emit("error", {"error": "Login Required"})
            return

        return f(*args, **kwargs)

    return wrapper


def socket_registered_only(f):
    """
    Restrict a Socket.IO event to registered users only.

    This decorator checks that:
    - a user is logged in
    - the account is not a guest account

    If either condition fails, an error event is emitted and the
    handler is not run.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            emit("error", {"error": "Login Required"})
            return

        if session.get("guest", False):
            emit("error", {"error": "Registered Account Required"})
            return

        return f(*args, **kwargs)

    return wrapper


def socket_in_game(f):
    """
    Restrict a Socket.IO event to users currently in a game.

    This decorator checks whether a game ID exists in the session.
    If not, an error event is emitted and the handler is not run.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("game_id"):
            emit("error", {"error": "Not In A Game"})
            return

        return f(*args, **kwargs)

    return wrapper