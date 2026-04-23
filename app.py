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

RULES = [
    {"label": "Allow Sets?", "name": "allow_sets", "control_type": "switch", "checked": True},
    {"label": "Allow Runs?", "name": "allow_runs", "control_type": "switch", "checked": True},

    {"label": "Max Meld Size (Run)", "name": "max_meld_size_run", "control_type": "text", "value": ""},
    {"label": "Min Initial Meld Score", "name": "min_initial_meld_score", "control_type": "text", "value": "0"},
    {"label": "Initial Meld Increment", "name": "initial_meld_increment", "control_type": "switch", "checked": False},

    {"label": "Wild Cards", "name": "wilds", "control_type": "text", "value": "[('Joker', 0)]"},
    {"label": "Wild Deadwood Score", "name": "wild_deadwood_score", "control_type": "text", "value": "25"},

    {"label": "Scoring Method (negative/positive)", "name": "scoring_method", "control_type": "text", "value": "negative"},

    {"label": "Ace Low", "name": "ace_low", "control_type": "switch", "checked": False},
    {"label": "Ace High", "name": "ace_high", "control_type": "switch", "checked": False},
    {"label": "Ace Both", "name": "ace_both", "control_type": "switch", "checked": True},
    {"label": "Ace Wrap Around", "name": "wrap_around", "control_type": "switch", "checked": False},

    {"label": "Ace High Score", "name": "ace_high_score", "control_type": "text", "value": "10"},

    {"label": "Initial Hand Size", "name": "initial_hand_size", "control_type": "text", "value": "14"},
    {"label": "Min Meld Size", "name": "min_meld_size", "control_type": "text", "value": "3"},
    {"label": "Max Meld Size (Set)", "name": "max_meld_size_set", "control_type": "text", "value": "4"},

    {"label": "Number of Decks", "name": "num_decks", "control_type": "text", "value": "2"},

    {"label": "Require Meld to Draw from Discard", "name": "require_melding_to_draw_from_disc", "control_type": "switch", "checked": True},
    {"label": "Require Meld to Lay Off", "name": "require_melding_to_lay_off", "control_type": "switch", "checked": True},

    {"label": "Allow Wild Replacement", "name": "allow_wild_replacement", "control_type": "switch", "checked": True},
    {"label": "Allow Wild Only Melds", "name": "allow_wild_only_melds", "control_type": "switch", "checked": False},

    {"label": "Prevent Discard Same Card", "name": "prevent_discard_same_card", "control_type": "switch", "checked": True},

    {"label": "Points for Winning", "name": "points_for_winning", "control_type": "text", "value": "25"},
    {"label": "Max Deck Shuffle", "name": "max_deck_shuffle", "control_type": "text", "value": ""},
    {"label": "Winner Deadwood", "name": "winner_deadwood", "control_type": "text", "value": "25"},

    {"label": "Max Players", "name": "max_players", "control_type": "text", "value": "4"},
]


def create_app():
    app = Flask(__name__)
    app.secret_key = "SecretKey@SoSecret"

    socketio = SocketIO(app, cors_allowed_origins="*")

    db = DatabaseService()
    game_service = GameService(db)

    auth_routes(game_service)
    game_routes(game_service, socketio)
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
    
    @app.route("/Login")
    def login():
        return render_template("Login.html")
    
    @app.route("/CustomRuleset")
    def ruleset():
        return render_template("CustomRuleset.html", rules=RULES)
    
    @app.route("/GameLobby")
    def gamelobby():
        return render_template("GameLobby.html", rules=RULES)

    @app.route("/FriendsList")
    def friendslist():
        return render_template("FriendsList.html")
    
    @app.route("/GameHistory")
    def gamehistory():
        return render_template("GameHistory.html")

    @app.route("/GameState")
    def gamestate():
        return render_template("GameState.html")

    return app, socketio

app, socketio = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)