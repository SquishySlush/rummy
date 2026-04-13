# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:14:09 2026

@author: Faisal Mustafa
"""

from flask import Flask
from flask_socketio import SocketIO
from game_logic.GameService import GameService
from SQLConnections.DatabaseService import DatabaseService

from auth_routes import auth_blueprint, auth_routes
from game_routes import game_blueprint, game_routes
from social_routes import social_blueprint, social_routes

from game_events import game_events
from social_events import social_events

def create_app():
    app = Flask(__name__)
    app.config.secret_key = "SecretKey@SoSecret"

    socketio = SocketIO(app, cors_allowed_origins="*")

    db = DatabaseService()
    game_service = GameService(db)

    auth_routes(game_service)
    game_routes(game_service)
    social_routes(game_service)

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(game_blueprint, url_prefix="/game")
    app.register_blueprint(social_blueprint, url_prefix="/social")

    game_events(socketio, game_service)
    social_events(socketio, game_service)

    return app, socketio

app, socketio = create_app()

if __name__ = "__main__":
    socketio.run(app, debug=True)