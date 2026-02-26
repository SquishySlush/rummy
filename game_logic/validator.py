# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:33:37 2026

@author: Faisal
"""

from game_logic.utils import sort_rank


class Validator:
    
    @staticmethod
    def validate_set(meld, ruleset):
        
        if len(meld) > ruleset.max_meld_size_set:
            return False
        
        ranks = []
        for card in meld:
            if card.is_wild != 1:
                ranks.append(card.rank)
        if len(set(ranks)) != len(ranks):
            return False
        
        else:
            suits = []
            for card in meld:
                
                if card.is_wild != 1:    
                    suits.append(card.suit.name)
                    
                if len(suits) == len(set(suits)):
                    return True
                else:
                    return False
    
    @staticmethod
    def validate_run(meld, ruleset):
        if len(meld) > ruleset.max_meld_size_run:
            return False
        cards = sort_rank(meld)
        card1_index = cards[0].index
        cards_suits =  []
        for card in cards:
            cards_suits.append(card.suit)
                
        if len(set(cards_suits)) > 1:
                return False
            
        for i in range(len(cards)):
            if card1_index + i != cards[i].index and not ruleset.is_wild(cards[i]):
                return False
        
        return True
    
    @staticmethod
    def validate_meld(cards, ruleset):
        if not len(cards) < ruleset.min_meld_size:
            if Validator.validate_set(cards, ruleset):
                return True,  'set'
            elif Validator.validate_run(cards, ruleset):
                return True, 'run'
        else:
            return False