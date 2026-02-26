# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 09:14:35 2026

@author: Faisal
"""

class Discard_pile:
    def __init__(self, cards):
        self.cards = cards
    
    def add_card(self, card):
        self.cards.append(card)
    
    def draw_top_card(self):
        return self.cards.pop()
    
    def split_discard_pile(self):
        card = self.cards.pop()
        cards = self.cards
        
        self.cards = card
        
        return cards
    
    def return_top_card(self):
        return self.cards[-1]