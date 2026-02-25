# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:33:37 2026

@author: Faisal
"""

from game_logic.utils import sort_rank


class validator:
    
    @staticmethod
    def validate_set(meld, ruleset):
        
        if len(meld) > ruleset.max_meld_size_set:
            return False,  "Too many cards"
        
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
    
    def validate_meld(self, cards, ruleset):
        if len(cards) < ruleset.min_meld_size:
            return False
        
        elif self.validate_set(cards, ruleset) or self.validate_run(cards, ruleset):
            return True        
    
    
    def melding(self, cards, ruleset):
        if self.validate_meld(cards, ruleset):
            return self.calculate_score(cards, ruleset)
        else:
            return False, "The meld is invalid"