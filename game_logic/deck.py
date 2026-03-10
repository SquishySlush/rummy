# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 10:02:52 2026

@author: Faisal
"""
from game_logic.utils import rank_index, Suit
from game_logic.card import Card
import random

class Deck:
    
    #when  the deck initiaises, creates a full deck of cards + jokers depending on the number of jokers chosen.
    
    def __init__(self, ruleset):
        
        #num_wilds is a list, where each index corresponds to an index in wilds.
        self.cards = []
        self.num_wilds =  ruleset.num_wilds
        
        for deck in ruleset.num_decks:
        #Removes wild cards from rank_index, so that it doesnt generate twice
            for card in ruleset.wilds:
                if card in rank_index:
                    del rank_index[card]
                
                
                for  rank in rank_index:
                    for suit in Suit:
                        self.cards.append(Card(rank, suit, 0))
    
        #Creates wild cards with
    
        for i in range(len(ruleset.wilds)): 
            for j in range(self.num_wilds[i]):
                self.cards.append(Card(ruleset.wilds[i], ''))
    
    #Shuffles the deck, by moving each card to a random position in the deck. This is used in unison with the draw function to have an O(1) when drawing a card, as otherwise it would have to choose a random card everytime, with an O(n) time complexity. 
    
    def shuffle(self):
        result = []
        for i in range(len(self.cards)):
            roll = random.randint(0, len(self.cards)-1)
            result.append(self.cards[roll])
            self.cards.remove(self.cards[roll])
        self.cards  = result
    
    
    #Returns the top card of the deck, while removing it.
    def draw(self):
        return self.cards.pop()
    
    #Returns the size of the deck
    def size(self):
        return len(self.cards)
    
    #Checks if the deck is empty
    def empty_check(self):
        if len(self.cards) == 0:
            return True
    
    #Appends a list of cards to the deck, e.g. all cards except top of a discard pile
    def add_cards(self, cards):
        self.cards.append(cards)