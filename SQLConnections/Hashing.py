# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:58:50 2026

@author: Faisal Mustafa
"""

import os


def simple_hash(input_str, salt):
    hash_vector = 2166136261
    
    combined = input_str + salt

    for char in combined:
        hash_vector ^= ord(char) #xor operation for each character in the hash value
        hash_vector *= 53383619654664048229
        hash_vector &= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        hash_vector ^= (hash_vector >> 13)
        hash_vector ^= (hash_vector << 7) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    
    return hash_vector

def hash_password(password):
    salt = os.urandom(8).hex()
    hash_value = simple_hash(password, salt)
    
    for h in range(1000):
        hash_value = simple_hash(str(hash_value), salt)
        
    return salt, format(hash_value, '032x')