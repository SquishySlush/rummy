# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 08:05:13 2026

@author: Faisal
"""

from enum import Enum

#Dictionary of ranks and indexes for both sorting and validating runs

rank_index = {
    "Ace"  : 0,
    "2" : 1,
    "3" : 2,
    "4" : 3,
    "5" : 4,
    "6" : 5,
    "7" : 6,
    "8" : 7,
    "9" : 8,
    "10" : 9,
    "Jack" : 10,
    "Queen" : 11,
    "King" : 12
    }



class Suit(Enum):
    
    #Creating an immutable enum for Suits
    
    Hearts = 1
    Clubs = 2
    Diamods = 3
    Spades = 4


class Card:
    def __init__(self, rank, suit):
        
        #Validating if the inputs are allowed
        
        if rank not in rank_index:
            raise ValueError(f"{rank} is not a valid rank")
        if suit not in Suit:
            raise ValueError(f"{suit} is not a valid suit")
        self.rank = rank
        self.suit = suit
    
    def return_rank_index(self): #RReturns the rank index, for sorting and meld validation. (Runs)
        return rank_index[self.rank]
    
    def __repr__(self): #Representation function for print(CardObject), such that it will output "Rank of Suit"
        return f"{self.rank} of {self.suit.value}"
    
    def __eq__(self, other): #Ewuality function changer, such that two cards with the same attributes are equal
        return self.rank == other.rank and self.suit == other.suit

    def return_value(self): #Returning the value of a card, for melds.
        if self.rank in ["Jack", "Queen", "King"]:
            return 10
        elif self.rank == "A":
            return 1
        else:
            return int(self.rank)
