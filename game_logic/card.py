# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 08:05:13 2026

@author: Faisal
"""
from game_logic.utils import Suit, rank_index, rank_score
import json

class Card:
    def __init__(self, rank, suit, ruleset):
        if rank not in rank_index and rank not in ruleset.wilds:  #Validating if the inputs are allowed
            raise ValueError(f"{rank} is not a valid rank")
        if rank not in ruleset.wilds:
            if suit not in Suit:
                raise ValueError(f"{suit} is not a valid suit")
                
        self.rank = rank
        self.suit = suit
        if rank in rank_index:
            self.index = int(rank_index[rank])
        else:
            self.index = None

    def return_rank_index(self): #Returns the rank index, for sorting and meld validation. (Runs)
        return int(rank_index[self.rank])
    
    def __repr__(self): #Representation function for print(CardObject), such that it will output "Rank of Suit"
        return f"{self.rank} of {self.suit.name}"
    
    def __eq__(self, other): #Ewuality function changer, such that two cards with the same attributes are equal
        return self.rank == other.rank and self.suit == other.suit

    def return_value(self, ruleset): #Returning the value of a card, for melds.
        if  ruleset.is_wild(self):
            return "wild"
        else:
            return rank_score[self.rank]
    
    def to_dict(self):
        return {
            'rank': self.rank,
            'suit': self.suit.name
            }
    
    @classmethod
    def from_dict(cls, data):
        rank = data['rank']
        suit = Suit[data['suit']]
        return cls(rank, suit)
    
    def to_json_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def from_json_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return Card.from_dict(data)

