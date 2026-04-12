# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 20:57:27 2026

@author: Faisal Mustafa
"""

import json

class GameRepository:
    
    @staticmethod
    def create_game(db, ruleset, status, seed):
        ruleset_string  = json.dumps(ruleset.to_dict())
        
        db.execute("INSERT INTO Games (ruleset, status, seed) VALUES (%s, %s, %s)",
                   (ruleset_string, status, seed))
        db.commit()
        game_id = db.cursor.lastrowid
        return True, game_id
    
    @staticmethod
    def change_status(db, game_id, status):
        db.execute("UPDATE Games SET status = %s WHERE game_id = %s",
                   (status, game_id))
        db.commit()
        
        return True, None
    
    @staticmethod
    def get_status(db, game_id):
        result = db.execute("SELECT status FROM Games WHERE game_id = %s",
                            (game_id))
        
        row = result.fetchone()
        
        if row is None:
            return None, "Game Not Found"
        return row
    
    @staticmethod
    def get_game(db, game_id):
        result = db.execute("SELECT * FROM Games WHERE game_id = %s",
                            (game_id,))
        
        row = result.fetchone()
        if row is None:
            return None, "Game Not Found"
        return row, None
    
    @staticmethod
    def get_ruleset(db, game_id):
        result = db.execute("SELECT ruleset FROM Games WHERE game_id = %s",
                            (game_id,))
        
        ruleset = result.fetchone()
        if ruleset is None:
            return None, "Game Not Found"
        return json.loads(ruleset["ruleset"]), None

    @staticmethod
    def delete_game(db, game_id):
        db.execute("DELETE FROM Games WHERE game_id = %s",
                   (game_id,))
        db.commit()
        
        return True, None
    
    @staticmethod
    def get_games_by_status(db, status):
        result = db.execute("SELECT game_id FROM Games WHERE status = %s",
                            (status,))
        
        rows = result.fetchall()
        if rows is None:
            return None, "No Games With That Status Found"
        return rows, None
    
    @staticmethod
    def get_seed(db, game_id):
        result = db.execute("SELECT seed FROM Games WHERE game_id = %s",
                            (game_id,))
        
        seed = result.fetchone()
        if seed is None:
            return None, "Game Does Not Exist"
        return seed["seed"], None