# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:33:37 2026

@author: Faisal
"""

from game_logic.utils import quicksort, split_wilds_non_wilds


class Validator:
    
    @staticmethod
    def validate_set(meld, ruleset):
        
        if ruleset.max_meld_size_set is not None and len(meld) > ruleset.max_meld_size_set:
            return False, "Meld Too Large"
        if len(meld) > ruleset.min_meld_size:
            return False, "Meld Too Small"
        
        suits = []
        ranks = []
        for card in meld:
            if not ruleset.is_wild(card):
                ranks.append(card.rank)
                suits.append(card.suit)
        
        if not ruleset.allow_wild_only_melds and len(ranks) == 0:
            return False, "Meld Contains Only Wild Cards"
        
        if len(set(ranks)) != 1:
            return False, "Multiple Ranks in 1 Set"
                
        if len(suits) != len(set(suits)):
            return False, "Multiple of the Same Suit in 1 Set"

        return True, meld
    
    @staticmethod
    def validate_run(meld, ruleset):
        if ruleset.max_meld_size_run is not None and len(meld) > ruleset.max_meld_size_run:
            return False, "Meld Too Large"
        if len(meld) > ruleset.min_meld_size:
            return False, "Meld Too Small"
        
        wilds, non_wilds = split_wilds_non_wilds(meld, ruleset)
        
        if not ruleset.allow_wild_only_melds and len(non_wilds) == 0:
            return False, "Meld Is All Wilds"
        
        
        indices = []
        suits = []
        for card in non_wilds:
            suits.append(card.suit)
            indices.append(card.return_rank_index())
        
        indices = quicksort(indices)
            
        if len(set(suits)) != 1:
            return False
        
        if len(indices) != len(set(indices)):
            return False
        
        min_index = min(indices)
        max_index = max(indices)
        span = max_index - min_index + 1
        gaps = span - len(non_wilds)
        
        if gaps <= len(wilds):
            return True
        
        has_ace = 0 in indices
        has_king = 12 in indices
        
        if has_ace:
            if ruleset.ace_high or ruleset.ace_both:

                adjusted_indices = []
                for index in indices:
                    if index == 0:
                        adjusted_indices.append(13)
                    else:
                        adjusted_indices.append(index)
            
                adjusted_indices = quicksort(adjusted_indices)
            
                min_index = min(adjusted_indices)
                max_index = max(adjusted_indices)
                span = max_index - min_index + 1
                gaps = span - len(non_wilds)    
                
            if gaps <= len(wilds):
                return True
            
            if ruleset.ace_wrap_around and has_king:
    
                low_indices = [index for index in indices if index <9]
                high_indices = [index for index in indices if index >= 10]
                    
                if len(low_indices) > 0 and len(high_indices) > 0:
                    low_span = max(low_indices) - min(low_indices) + 1
                    high_span = max(high_indices) - min(high_indices) + 1
                        
                    total_gaps = (low_span - len(low_indices)) + (high_span - len(high_indices))
                    if total_gaps <= len(wilds):
                        return True
                
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
    
    