# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:14:09 2026

@author: Faisal Mustafa
"""

from flask import Flask, render_template
from flask_socketio import SocketIO
from game_logic.GameService import GameService
from SQLConnections.DatabaseService import DatabaseService

from FrontEnd.auth_routes import auth_blueprint, auth_routes
from FrontEnd.game_routes import game_blueprint, game_routes
from FrontEnd.social_routes import social_blueprint, social_routes

from FrontEnd.game_events import game_events
from FrontEnd.social_events import social_events

def create_app():
    app = Flask(__name__)
    app.secret_key = "SecretKey@SoSecret"

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

    @app.route("/")
    def home_page():
        return render_template("MainMenu.html")

    @app.route("/SignUp")
    def signup_page():
        return render_template("SignUp.html")

    return app, socketio

app, socketio = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)