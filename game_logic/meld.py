# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 09:06:53 2026

@author: Faisal
"""

from game_logic.utils import sort_rank
from game_logic.ruleset import Ruleset

class Meld:
    def __init__(self, cards, meld_type):
        self.cards = cards
        self.meld_type = meld_type #2 Meld types, set or run.
    
    def wild_assignment_run(self, cards, ruleset):
        non_wilds = []
        wilds = []
        wild_assignments = {} #A dictionary of wild cards, with their rank_index and suit
        
        
        #Creates a list of wild and non wild cards
        for card in cards:
            if Ruleset.is_wild(card):
                wilds.append(card)
            else:
                non_wilds.append(card)       
        
        #Creates a sorted list of the indices of non wild cards
        sorted_non_wilds = sort_rank(non_wilds)
        indices = []
        for  card in sorted_non_wilds:
            indices.append(card.return_rank_index())
        
        #Creates a  list of the expected indices of the non wild cards
        range_indexes = range(indices[0], indices[-1])
        
        
        #Finds the missing indices between cards, such that a card, wild, card is accounted for.
        missing_indices = []
        for index in indices:
            if index not in range_indexes:
                missing_indices.append(index)
        
        for missing_index in missing_indices:
        if len(wilds) - 
            
        
        
        