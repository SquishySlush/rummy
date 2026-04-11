# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:18:22 2026

@author: Faisal Mustafa
"""
from SQLConnections.Hashing import hash_password

class UserRepository:
    
    @staticmethod
    def create_user(db, username, password, email):
        
        if UserRepository._username_exists(db, username):
            return False, "Username Exists"

        salt, hashword = hash_password(password)
        
        db.execute(
            "INSERT INTO Users(username, password, email, salt) VALUES (%s, %s, %s, %s)",
            (username, hashword, email, salt))
        db.commit()
        
        return True, "User Created"
    
    @staticmethod
    def _username_exists(db, username):
        result = db.execute(
            "SELECT 1 FROM Users WHERE username = %s",
            (username,)
            )
        
        return result.fetchone() is not None
    
    @staticmethod
    def get_user_by_username(db, username):
        result = db.execute("SELECT * FROM Users WHERE username = %s",
                            (username,))
        
        row = result.fetchone()
        if row is None:
            return None, "User Not Found"
        return row, None
    
    @staticmethod
    def get_user_by_id(db, user_id):
        result = db.execute("SELECT * FROM Users WHERE user_id = %s",
                            (user_id,))
        
        row = result.fetchone()
        if row is None:
            return False, "User Not Found"
        else:
            return row, None
    
    @staticmethod
    def change_password(db, user_id, password, new_password):
        result, error = UserRepository.verify_password(password, user_id)
        
        if result:
            hashword = hash_password(new_password)
            db.execute("UPDATE Users SET password = %s WHERE user_id = %s",
                       (hashword, user_id))
            db.commit()
            return result, None
        else:
            return result, error
    
    @staticmethod
    def change_username(db, user_id, new_username):
        db.execute("UPDATE Users SET username = %s WHERE user_id = %s",
                   (new_username, user_id))
        db.commit()
        
        return True, None
    
    
    @staticmethod
    def delete_user(db, user_id):
        db.execute("DELETE FROM Users WHERE user_id = %s",
                   (user_id,))
        db.commit()
        
        return True, None
    
    @staticmethod
    def verify_password(db, password, user_id):
        result = db.execute("SELECT password FROM Users WHERE user_id = %s",
                              (user_id,))
        
        row = result.fetchone()
        
        if row is None:
            return False, "User Not Found"
        
        if hash_password(password) == row[0]:
            return True, None
        
        return False, "Password incorrect"