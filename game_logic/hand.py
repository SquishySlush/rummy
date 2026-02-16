# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 09:34:56 2026

@author: Faisal
"""

from game_logic.card import Card, Suit

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def remove_card(self, card):
        self.cards.remove(card)
    
    def sort_rank(self, items):
        if len(items) <= 1:
            return items

        pivot_card = items.pop()
        pivot_index = pivot_card.return_rank_index()
        items_greater = []
        items_lower = []
        
        for i in items:
            if i.return_rank_index > pivot_index:
                items_greater.append(i)
            else:
                items_lower.append(i)
        return self.sort_rank(items_lower) + [pivot_card] + self.sort_rank(items_greater)