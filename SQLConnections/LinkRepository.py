# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 23:19:05 2026

@author: Faisal Mustafa
"""

class LinkRepository:
    
    @staticmethod
    def create_game_history(db, user_id, game_id, result, role):
        db.execute(
            "INSERT INTO GameHistory(user_id, game_id, result, role) VALUES (%s, %s, %s, %s)",
            (user_id, game_id, result, role))
        db.commit()
    
    @staticmethod
    def get_game_history_by_player(db, user_id):
        result = db.execute("SELECT * FROM GameHistory WHERE user_id = %s",
                            (user_id,))
        
        rows = result.fetchall()
        if rows == []:
            return None, "No Game History Found"
        return rows, None
    
    @staticmethod
    def get_game_history_by_game(db, game_id):
        result = db.execute("SELECT * FROM GameHistory WHERE game_id = %s",
                            (game_id,))
        
        rows = result.fetchall()
        if rows == []:
            return None, "No Game History Found"
        return rows, None
    
    @staticmethod
    def update_game_history(db, user_id, game_id, result):
        db.execute("UPDATE GameHistory SET result = %s WHERE user_id = %s AND game_id = %s",
                   (result, user_id, game_id))
        db.commit()
        
        return True, None
    
    @staticmethod
    def create_friends_list(db, user_id, friend_id):
        db.execute(
            "INSERT INTO FriendsList(user_id, friend_id) VALUES (%s, %s)",
            (user_id, friend_id))
        db.commit()
    
    @staticmethod
    def update_friend_status(db, user_id, friend_id, status):
        db.execute("UPDATE FriendsList SET status = %s WHERE user_id = %s AND friend_id = %s",
                   (status, user_id, friend_id))
        db.commit()
        
        return True, None
    
    @staticmethod
    def get_friends(db, user_id):
        result = db.execute("SELECT * FROM FriendsList WHERE user_id = %s",
                            (user_id,))
        
        rows = result.fetchall()
        if rows == []:
            return None, "No Friends Found"
        return rows, None
    
    @staticmethod
    def get_pending_requests(db, user_id, status):
        result = db.execute("SELECT * FROM FriendsList WHERE user_id = %s AND status = %s",
                            (user_id, status))
        
        rows = result.fetchall()
        if rows == []:
            return None, "No Friends Found"
        return rows, None
    
    @staticmethod
    def delete_friend(db, user_id, friend_id):
        db.execute("DELETE FROM FriendsList WHERE user_id = %s AND friend_id = %s",
                   (user_id, friend_id))
        db.commit()
        
        return True, None