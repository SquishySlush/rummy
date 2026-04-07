# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 10:02:52 2026

@author: Faisal
"""
from game_logic.utils import rank_index, Suit
from game_logic.card import Card
import random

local_rank_index = rank_index.copy()

class Deck:
    
    #when  the deck initiaises, creates a full deck of cards + jokers depending on the number of jokers chosen.
    
    def __init__(self, ruleset, seed=None): #Default creates no seed
        if seed is None:
            seed = random.SystemRandom().randint(0, 2**32 -1) #if no seed is selected, use the OS' random number generator to make a 32bit seed
        
        #num_wilds is a list, where each index corresponds to an index in wilds.
        self.cards = []
        self.seed = seed
        self.rng = random.Random(seed)
        
        for deck in range(ruleset.num_decks):
            for rank in rank_index:
                if rank not in ruleset.wilds:
                    for suit in Suit:
                        self.cards.append(Card(rank, suit, ruleset))
        for wild, num_wild in ruleset.wilds:
            for i in range(num_wild):
                self.cards.append(Card(wild, None, ruleset))
    

    
    def shuffle(self): #Shuffles the deck, by moving each card to a random position in the deck
        for i in range(len(self.cards) -1, 0, -1): #goes backwards through the list, random card is chosen and swaps place with the current i
            roll = self.rng.randint(0, i)
            self.cards[i], self.cards[roll] = self.cards[roll], self.cards[i]    
    
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
        self.cards.extend(cards)

