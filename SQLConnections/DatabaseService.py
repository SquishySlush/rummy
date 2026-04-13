# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 15:32:38 2026

@author: Faisal Mustafa
"""

from DBConnections import dbconnection
from UserRepository import UserRepository
from GameRepository import GameRepository
from MoveRepository import MoveRepository
from LinkRepository import LinkRepository
from Hashing import hash_password

class DatabaseService:
    
    def __init__(self):
        self.db = dbconnection()
    
    def close(self):
        self.db.close()
        
    def sign_up(self, username, password, email):
        
        #Returns True, "User Created" on success, False, "Username Exists" If
        #Username is already taken
        return UserRepository.create_user(self.db, username, password, email)
    
    def log_in(self, username, password):
        
        user, error = UserRepository.get_user_by_username(self.db, username)
        
        
        if user is None: #Verifies if the username exists
            return False, error
        
        stored_hash = user["password"]
        salt = user["salt"]
        
        _, hashed_password = hash_password(password, salt)
        
        if hashed_password == stored_hash:
            return user, None
        return None, "Incorrect Password" #Verfies correct password
    
    def get_user_by_id(self, user_id):
        return UserRepository.get_user_by_id(self.db, user_id)
    
    def change_password(self, user_id, old_password, new_password):
        return UserRepository.change_password(self.db, user_id, old_password, new_password)    
    
    def change_username(self, user_id, new_username):
        return UserRepository.change_username(self.db, user_id, new_username)
    
    def delete_user(self, user_id):
        
        MoveRepository.delete_all_moves_by_user(self.db, user_id)
        LinkRepository.delete_friends_by_user(self.db, user_id)
        LinkRepository.delete_all_game_history_by_user(self.db, user_id)
        
        return UserRepository.delete_user(self.db, user_id)
    
    def send_friend_request(self, user_id, friend_id):
        
        if not UserRepository.get_user_by_id(self.db, user_id):
            return False, "Requesting User Not Found"
        if not UserRepository.get_user_by_id(self.db, friend_id):
            return False, "Target User Not Found"
        
        LinkRepository.create_friends_list(self.db, user_id, friend_id)
        return True, None
    
    def accept_friend_request(self, user_id, friend_id):
        return LinkRepository.update_friend_status(self.db, user_id, friend_id, "Accepted")
    
    def reject_friend_request(self, user_id, friend_id):
        return LinkRepository.delete_friend(self.db, user_id, friend_id)
    
    def get_friends(self, user_id):
        return LinkRepository.get_friends_by_status(self.db, user_id, "Accepted")
    
    def get_pending_requests(self, user_id):
        return LinkRepository.get_friends_by_status(self.db, user_id, "Pending")
    
    def create_game(self, ruleset, seed):
        return GameRepository.create_game(self.db, ruleset, "LOBBY", seed)
    
    def start_game(self, game_id):
        return GameRepository.change_status(self.db, game_id, "In Progress")
    
    def get_game(self, game_id):
        return GameRepository.get_game(self.db, game_id)
    
    def get_ruleset(self, game_id):
        return GameRepository.get_ruleset(self.db, game_id)
    
    def get_seed(self, game_id):
        return GameRepository.get_seed(self.db, game_id)
    
    def get_games_in_lobby(self):
        return GameRepository.get_games_by_status(self.db, "In Lobby")
    
    def pause_game(self, game_id):
        return GameRepository.change_status(self.db, game_id, "Paused")

    def unpaused_game(self, game_id):
        return GameRepository.change_status(self.db, game_id, "In Progress")
    
    def get_paused_games_by_user(db, user_id):
        result = db.execute(
            """SELECT Games.game_id FROM Games 
            JOIN GameHistory ON Games.game_id = GameHistory.game_id
            WHERE GameHistory.user_id = %s AND Games.status = 'Paused'""",
            (user_id,))
    
        rows = result.fetchall()
        if rows == []:
            return None, "No Paused Games Found"
        return rows, None
    
    def get_lobbies(self):
        return GameRepository.get_games_by_status(self.db, "In Lobby")
    
    def get_game_status(self, game_id):
        return GameRepository.get_status(self.db, game_id)
    
    def delete_game(self, game_id):
        MoveRepository.delete_all_moves_in_game(self.db, game_id)
        return GameRepository.delete_game(self.db, game_id)
    
    def add_player_to_game(self, user_id, game_id, role):
        LinkRepository.create_game_history(self.db, user_id, game_id, "In Progress", role)


    def record_game_result(self, user_id, game_id, result):
        return LinkRepository.update_game_history(self.db, user_id, game_id, result)
    
    def get_player_history(self, user_id):
        return LinkRepository.get_game_history_by_player(self.db, user_id)
    
    def get_game_players(self, game_id):
        return LinkRepository.get_game_history_by_game(self.db, game_id)
    
    def add_move(self, game_id, user_id, move_type, card=None, meld_index=None):
        move_number, _ = MoveRepository.get_move_count(self.db, game_id)    
        move_number += 1
        
        return MoveRepository.add_move(self.db, game_id, user_id, move_number, move_type, card, meld_index)
    
    def get_moves(self, game_id):
        return MoveRepository.get_moves_by_game(self.db, game_id)
    
    def get_move_count(self, game_id):
        return MoveRepository.get_move_count(self.db, game_id)