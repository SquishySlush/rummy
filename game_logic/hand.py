# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 09:34:56 2026

@author: Faisal
"""

from game_logic.card import Card, Suit

class Hand:
    def __init__(self):
        self.cards = [] #Initialises hand as a list of cards
        self.selected_card = []
    
    def __repr__(self):
        for i in self.cards:
            print(i)
        return
        
    def add_card(self, card):
        self.cards.append(card)
    
    def remove_card(self, card):
        self.cards.remove(card)
    
    def select_card(self, card):
        self.selected_card.append(card)
    
    def deselect_card(self, card):
        self.selected_card.remove(card)
    
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
    
    def sort_suit(self, items):
        items_hearts = []
        items_clubs = []
        items_diamonds = []
        items_spades = []
        for i in items:
            if i.suit.value == 1:
                items_hearts.append(i)
            if i.suit.value == 2:
                items_clubs.append(i)
            if i.suit.value == 3:
                items_diamonds.append(i)
            if i.suit.value == 4:
                items_spades.append(i)
        
        return self.sort_rank(items_hearts) + self.sort_rank(items_clubs)  + self.sort_rank(items_diamonds) + self.sort_rank(items_spades)