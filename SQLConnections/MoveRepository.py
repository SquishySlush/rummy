# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 21:27:13 2026

@author: Faisal Mustafa
"""

import json

class MoveRepository:
    
    @staticmethod
    def add_move(db, game_id, user_id, move_number, move_type, card=None, meld_index=None):
        card_string = json.dumps(card.to_dict()) if card is not None else None
        
        db.execute("INSERT INTO Moves (game_id, user_id, move_number, move_type, card, meld_index) VALUES (%s, %s, %s, %s, %s, %s)",
                   (game_id, user_id, move_number, move_type, card_string, meld_index))
        
        db.commit()
        move_id = db.cursor.lastrowid
        return True, move_id
    
    @staticmethod
    def get_moves_by_game(db, game_id):
        result = db.execute("SELECT * FROM Moves WHERE game_id = %s ORDER BY move_number ASC",
                            (game_id,))
        
        rows = result.fetchall()
        if rows == []:
            return None, "No Game Exists"
        return rows, None
    
    @staticmethod
    def delete_all_moves_in_game(db, game_id):
        
        db.execute("DELETE FROM Moves WHERE game_id = %s",
                   (game_id,))
        db.commit()
        
        return True, None
    
    @staticmethod
    def get_moves_by_player(db, user_id):
        result = db.execute("SELECT move_id FROM Moves WHERE user_id = %s",
                            (user_id,))
        
        rows = result.fetchall()
        if rows == []:
            return None, "No User Exists"
        return rows, None
    
    @staticmethod
    def get_move_count(db, game_id):
        result = db.execute("SELECT COUNT(*) FROM Moves WHERE game_id = %s",
                   (game_id,))
        
        count = result.fetchone()
        return count[0], None