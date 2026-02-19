# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 09:34:56 2026

@author: Faisal
"""

from game_logic.utils import sort_rank

class Hand:
    def __init__(self):
        self.cards = [] #Initialises hand as a list of cards
        self.selected_cards = []
    
    def __repr__(self):
        for card in self.cards:
            card_strings  = [str(card) for card in self.cards] #Creates a list of str(card) from self.cards
        if len(self.selected_cards) > 0:
            for card in self.selected_cards:
                selected_cards_strings = [str(card) for card in self.selected_cards]
            return (', '.join(card_strings) + "\n Selected Cards:" + ', '.join(selected_cards_strings)) #Joins the objects of the list with ', ', such that it appears object, object, ...
        else:
            return ', '.join(card_strings)
        
        
    def add_card(self, card): #appends card to list
        self.cards.append(card)
    
    def remove_card(self, card): #removes card object from the list
        self.cards.remove(card)
    
    def select_card(self, card): #Adds card object to a seperate list called selected_cards
        self.selected_cards.append(card)
    
    def deselect_card(self, card): #removes card from selected_cards list
        self.selected_cards.remove(card)
        
    def deselect_all(self): #Deselects all cards by setting the selected cards to an empty list
        self.selected_cards = []
    
    def sort_by_rank(self):
        self.cards = sort_rank(self.cards)
    
    def sort_by_suit(self):
        self.cards = self.sort_suit(self.cards)
    
    def sort_suit(self, items): #Split cards by suit, before sorting each on its own. It then sorts each individually using sort_rank, before joining them together.
        items_hearts = []
        items_clubs = []
        items_diamonds = []
        items_spades = []
        for i in items:
            if i.suit.value == 0:
                items_hearts.append(i)
            if i.suit.value == 1:
                items_clubs.append(i)
            if i.suit.value == 2:
                items_diamonds.append(i)
            if i.suit.value == 3:
                items_spades.append(i)
        
        return self.sort_rank(items_hearts) + self.sort_rank(items_clubs)  + self.sort_rank(items_diamonds) + self.sort_rank(items_spades)