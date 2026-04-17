
from flask import jsonify, session
from functools import wraps

def registered_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error" : "Account Required"}), 401
        if session.get("guest", False):
            return jsonify({"error": "registered Account Required"})
        return f(*args, **kwargs)
    return wrapper


def user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error" : "Account Required"}), 401
        return f(*args, **kwargs)
    return wrapper