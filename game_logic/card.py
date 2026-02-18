# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 08:05:13 2026

@author: Faisal
"""
from game_logic.utils import Suit, rank_index

class Card:
    def __init__(self, rank, suit, is_wild):
        
        self.is_wild = is_wild #Is the card a wild card, 1 or 0
        
        if self.is_wild == 0: #if a card is a wild card, do not check suit or rank validity.
            if rank not in rank_index:         #Validating if the inputs are allowed
                raise ValueError(f"{rank} is not a valid rank")
            if suit not in Suit:
                raise ValueError(f"{suit} is not a valid suit")
                
        self.rank = rank
        self.suit = suit
    
    def return_rank_index(self): #RReturns the rank index, for sorting and meld validation. (Runs)
        return int(rank_index[self.rank])
    
    def __repr__(self): #Representation function for print(CardObject), such that it will output "Rank of Suit"
        return f"{self.rank} of {self.suit.name}"
    
    def __eq__(self, other): #Ewuality function changer, such that two cards with the same attributes are equal
        return self.rank == other.rank and self.suit == other.suit

    def return_value(self): #Returning the value of a card, for melds.
        if self.rank in ["Jack", "Queen", "King"]:
            return 10
        else:
            return int(self.rank)