# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:14:09 2026

@author: Faisal Mustafa
"""

from flask import Flask
from flask_socketio import SocketIO
from game_logic.GameService import GameService
from SQLConnections.DatabaseService import DatabaseService


app = Flask(__name__)
app.secret_key = "SecretKey@SoSecret"

socketio = SocketIO(app)

db = DatabaseService
game_service = GameService(db)