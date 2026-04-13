
from flask import jsonify, session

def registered_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"message", "Guests Cannto Do This"}), 403
        retrun f(*args, **kwargs)
    return wrapper

