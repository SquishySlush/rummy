# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:33:37 2026

@author: Faisal
"""

from game_logic.utils import sort_rank


class Validator:
    
    @staticmethod
    def validate_set(meld, ruleset):
        
        if ruleset.max_meld_size_set and len(meld) > ruleset.max_meld_size_set:
            return False
        
        ranks = []
        for card in meld:
            if not ruleset.is_wild(card):
                ranks.append(card.rank)
        if len(set(ranks)) != 1:
            return False
        
        
        suits = []
        for card in meld:
                
            if not ruleset.is_wild(card):    
                suits.append(card.suit.name)
                
        if len(suits) == len(set(suits)):
            return True
        else:
            return False
    
    @staticmethod
    def validate_run(meld, ruleset):
        if ruleset.max_meld_size_run and len(meld) > ruleset.max_meld_size_run:
            return False
        
        wilds = []
        non_wilds = []
        for card in meld:
            if ruleset.is_wild(card):
                wilds.append(card)
            else:
                non_wilds.append(card)
        
        if len(non_wilds) == 0:
            return False
        
        suits = []
        for card in non_wilds:
            suits.append(card.suit.name)
        
        if len(set(suits)) != 1:
            return False
        
        sorted_cards = sort_rank(non_wilds)
            
        indices = []
        for card in sorted_cards:
            indices.append(card.return_rank_index())
        
        if len(indices) != len(set(indices)):
            return False
        
        min_index = min(indices)
        max_index = max(indices)
        span = max_index - min_index + 1
        gaps = span - len(non_wilds)
        
        if gaps <= len(wilds):
            return True
        
        if ruleset.ace_high or ruleset.ace_both:
            has_ace = 0 in indices
            
            if has_ace:
                adjusted_indices = []
                for index in indices:
                    if index == 0:
                        adjusted_indices.append(13)
                    else:
                        adjusted_indices.append(index)
        
            adjusted_indices.sort()
            
            min_index = min(indices)
            max_index = max(indices)
            span = max_index - min_index + 1
            gaps = span - len(non_wilds)    
            
            if gaps <= len(wilds):
                return True
        
        if ruleset.ace_wrap_around:
            has_ace = 0 in indices
            has_king = 12 in indices
            
            if has_ace and has_king:
                low_indices = [index for index in indices if index <5]
                high_indices = [index for index in indices if index >= 10]
                
                if len(low_indices) > 0 and len(high_indices) > 0:
                    low_span = max(low_indices) - min(low_indices) + 1
                    high_span = max(high_indices) - min(high_indices) + 1
                    
                    total_gaps = (low_span - len(low_indices)) + (high_span - len(high_indices))
                    if total_gaps <= len(wilds):
                        return True, 
                
        return False
    
    
    @staticmethod
    def validate_meld(cards, ruleset):
        if len(cards) > ruleset.min_meld_size:
            if Validator.validate_set(cards, ruleset):
                return True,  'set'
            elif Validator.validate_run(cards, ruleset):
                return True, 'run'
        else:
            return False, None