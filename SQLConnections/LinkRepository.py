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
            return False, "No Game History Found"
        return True, rows
    
    @staticmethod
    def get_game_history_by_game(db, game_id):
        result = db.execute("SELECT * FROM GameHistory WHERE game_id = %s",
                            (game_id,))
        
        rows = result.fetchall()
        if rows == []:
            return False, "No Game History Found"
        return True, rows
    
    
    @staticmethod
    def delete_all_game_history_by_user(db, user_id):
        
        db.execute("DELETE FROM GameHistory WHERE user_id = %s",
                   (user_id,))
        db.commit()
    
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
    def update_friend_status(db, sender_id, receiver_id, status):
        result = db.execute(
        """UPDATE FriendsList SET status = %s 
        WHERE user_id = %s AND friend_id = %s AND status = 'Pending'""",
        (status, sender_id, receiver_id))
    
        if result.rowcount == 0:
            return False, "Request Not Found Or Not Authorised"
    
        db.execute(
            """INSERT INTO FriendsList (user_id, friend_id, status)
            VALUES (%s, %s, %s)""",
            (receiver_id, sender_id, status))

        db.commit()
        
        return True, None

    
    @staticmethod
    def get_friends(db, user_id):
        result = db.execute("SELECT * FROM FriendsList WHERE user_id = %s AND status = Accepted",
                            (user_id,))
        
        rows = result.fetchall()
        if rows == []:
            return False, "No Friends Found"
        return True, rows
    
    @staticmethod
    def get_friends_by_status(db, user_id, status):
        result = db.execute("SELECT * FROM FriendsList WHERE user_id = %s AND status = %s",
                            (user_id, status))
        
        rows = result.fetchall()
        if rows == []:
            return False, "No Friends Found"
        return True, rows
    
    @staticmethod
    def get_pending_requests_for_user(db, user_id):
        result = db.execute(
            """
            SELECT * FROM FriendsList
            WHERE status = 'Pending'
            AND (user_id = %s OR friend_id = %s)
            """,
            (user_id, user_id)
        )

        rows = result.fetchall()
        if rows == []:
            return False, "No Pending Requests Found"
        return True, rows

    @staticmethod
    def delete_friend(db, user_id, friend_id):
        db.execute("DELETE FROM FriendsList WHERE user_id = %s AND friend_id = %s",
                   (user_id, friend_id))
        db.commit()
        
        return True, None
    
    @staticmethod
    def delete_friends_by_user(db, user_id):
        db.execute("DELETE FROM FriendsList WHERE user_id = %s",
                   (user_id,))
        db.commit()