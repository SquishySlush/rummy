# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 09:14:35 2026

@author: Faisal
"""

class Discard_pile:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def draw_top_card(self):
        return self.cards.pop()
    
    def split_discard_pile(self):
        
        #Makes the top card the discard pile, the only card in the discard pile. All other cards are returned. This is when the deck has 0 cards, so all other cards can be appended to the deck, and then reshuffled.
        
        if len(self.cards) <= 1:
            return []
            
        top_card = self.cards[-1]
        cards_to_reshuffle = self.cards[:-1]
        
        self.cards = [top_card]
        
        return cards_to_reshuffle
    
    def return_top_card(self):
        return self.cards[-1]
    
    def is_empty(self):
        if len(self.cards) == 0:
            return True
        else:
            return False