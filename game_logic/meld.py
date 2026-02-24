# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 09:06:53 2026

@author: Faisal
"""

from game_logic.utils import sort_rank, index_rank, Suit

class Meld:
    def __init__(self, cards, meld_type, ruleset):
        self.cards = cards
        self.meld_type = meld_type #2 Meld types, set or run.
        self.wild_assignments = {} #A dictionary of wild cards, with their rank_index and suit
        
        if meld_type == 'run':
            self._wild_assignment_run(cards, ruleset)
        else:
            self._wild_assignment_set(cards, ruleset)
    def _wild_assignment_run(self, cards, ruleset):
        non_wilds = []
        wilds = []        
        
        #Creates a list of wild and non wild cards
        for card in cards:
            if ruleset.is_wild(card):
                wilds.append(card)
            else:
                non_wilds.append(card)       
        
        #Creates a sorted list of the indices of non wild cards
        sorted_non_wilds = sort_rank(non_wilds)
        indices = []
        for  card in sorted_non_wilds:
            indices.append(card.return_rank_index())
        
        #Creates a  list of the expected indices of the non wild cards
        range_indexes = range(indices[0], indices[-1] +1)
        
        #Finds the missing indices between cards, such that a card, wild, card is accounted for.
        missing_indices = []
        for index in range_indexes:
            if index not in indices:
                missing_indices.append(index)
        
        for wild, missing_index in zip(wilds, missing_indices):
            self.wild_assignments[wild] = {
                "rank_index": missing_index,
                "rank": index_rank[missing_index],
                "suit": sorted_non_wilds[0].suit}
        
        if len(wilds) > 0:
            for i, wild in enumerate(wilds):
                self.wild_assignments[wild] = {
                    'rank_index': min(indices) - (len(wilds) - i),
                    'rank': index_rank[min(indices) - (len(wilds) - i)],
                    'suit': sorted_non_wilds[0].suit}
    
    
    def _wild_assignment_set(self, cards, ruleset):
        suits = [Suit.Hearts, Suit.Clubs, Suit.Diamonds, Suit.Spades]
        
        non_wilds = []
        
        wilds = []
        
        for card in cards:
            if ruleset.is_wild(card):
                wilds.append(card)
            else:
                non_wilds.append(card)
                
        
        non_wild_suits = []
        
        for card in non_wilds:
            non_wild_suits.append(card.suit)
        
        missing_suits = []
        
        for suit in suits:
            if suit not in non_wild_suits:
                missing_suits.append(suit)
        
        for i, wild in enumerate(wilds):
            self.wild_assignments[wild] = {
                'rank_index' : non_wilds[0].return_rank_index,
                'rank' : index_rank[cards[0].return_rank_index],
                'suit' : missing_suits[i]}
        
        