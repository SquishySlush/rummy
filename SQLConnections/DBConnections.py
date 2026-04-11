# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:09:13 2026

@author: Faisal Mustafa
"""

import mysql.connector

class dbconnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            password = 'pass123',
            database = 'house_rummy')
        
        self.cursor = self.connection.cursor()
    
    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor
    
    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.cursor.close()
        self.connection.close