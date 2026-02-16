# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 09:34:56 2026

@author: Faisal
"""

from game_logic.card import Card, Suit,

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def remove_card(self, card):
        self.cards.remove(card)
    
    