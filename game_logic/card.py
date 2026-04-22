# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 08:05:13 2026

@author: Faisal
"""
from game_logic.utils import Suit, rank_index, rank_score
import json

class Card:
    def __init__(self, rank, suit, ruleset):
        """
        Initialises the card object, validating it against the known ranks known.

        Args:
            Rank (string): rank of the card.
            Suit (enum): an enum object for the suit, as they are immutable.
            Ruleset (ruleset object): for validation.

        Returns:
            card object
        """


        if rank not in rank_index and rank not in ruleset.wilds:
        #Checks if rank is in the valid ranks.

            raise ValueError(f"{rank} is not a valid rank")
        
        if rank not in ruleset.wilds:
        #If the rank is not a wildcard, then it must have a suit, otherwise it just continues

            if suit not in Suit:
            #Checks if suit is a valid suit enum

                raise ValueError(f"{suit} is not a valid suit")
                
        self.rank = rank
        self.suit = suit
        if rank in rank_index:
            self.index = int(rank_index[rank]) 
            #If the rank is not a wildcard, then added a rank index
        else:
            self.index = None 
            #If the card is a wildcard, no rank index

    def return_rank_index(self):
        """
        Returns the index of the rank of the card object, used for run validation

        Args:
            self
        
        Returns:
            Integer: index of rank
        """
        return int(rank_index[self.rank])
    
    def __repr__(self):
        """
        Defines the representation of the card in text form, used for testing.

        Args:
            self
        
        Returns:
            String: Rank of Suits, e.g. King of Clubs
        """
        return f"{self.rank} of {self.suit.name}"
    
    def __eq__(self, other):
        """
        Defines the equality of two card objects, used for validation elsewhere

        Args:
            self
        
        Returns:
            Boolean, True if equal, False if not equal
        """
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
    def from_dict(cls, data, ruleset):
        rank = data['rank']
        suit = Suit[data['suit']]
        return cls(rank, suit, ruleset)
    
    def to_json_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def from_json_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return Card.from_dict(data)

