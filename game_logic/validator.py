# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:33:37 2026

@author: Faisal
"""

from game_logic.utils import sort_rank


class validator:

    def validate_set(cards, ruleset):
        if len(cards) > ruleset.max_meld_size_set:
            return False
        ranks = []
        for card in cards:
            if card.is_wild != 1:
                ranks.append(card.rank)
            if len(ranks) != len(set(ranks)):
                return False
            else:
                suits = []
                for card in cards:
                    if card.is_wild != 1:    
                        suits.append(card.suit.name)
                    if len(suits) == len(set(suits)):
                        return True
                else:
                    return False
    
    def validate_run(cards, ruleset):

        cards = sort_rank(cards)
        card1_index = cards[0].index
        for card in cards:
            if card.rank != cards[0].rank and card.is_wild != 1:
                return False
            for i in range(len(cards)):
                if card1_index + i != cards[i].index and cards[i].is_wild != 1:
                    return False      
        return True
    
    def validate_meld(self, cards, ruleset):
        if len(cards) < ruleset.min_meld_size:
            return False
        elif self.validate_set(cards, ruleset) or self.validate_run(cards, ruleset):
            return True
    
    def meld_score(cards):
        

