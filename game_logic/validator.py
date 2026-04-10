# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:33:37 2026

@author: Faisal
"""

from game_logic.utils import quicksort, split_wilds_non_wilds
from enum import Enum

class Moves(Enum):
    
    #Creates an immutable enum for the available moves, along with their notation
    
    Draw_Deck = "Draw From Deck"
    Draw_Discard = "Draw From Discard Pile"
    Discard = "Discard Card"
    Meld = "Meld Cards"
    Lay_Off = "Lay Off Card"    
    Deck_Shuffle = "Shuffles the Deck"
    
class MeldTypes(Enum):
    
    RUN = "run"
    SET = "set"

class Validator:
    
    @staticmethod
    def validate_set(meld, ruleset):
        if meld.meld_type != MeldTypes.SET:
            return False, "Not Valid Meld Type"
        
        if ruleset.max_meld_size_set is not None and len(meld) > ruleset.max_meld_size_set:
            return False, "Meld Too Large"
        if len(meld) < ruleset.min_meld_size:
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

        return True, MeldTypes.SET
    
    @staticmethod
    def validate_run(meld, ruleset):
        
        if meld.meld_type != MeldTypes.RUN:
            return False, "Not Valid Meld Type"
        
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
            return False, "Multiple suits"
        
        if len(indices) != len(set(indices)):
            return False, "Multiples of the same rank"
        
        min_index = min(indices)
        max_index = max(indices)
        span = max_index - min_index + 1
        gaps = span - len(non_wilds)
        
        if gaps <= len(wilds):
            return True, MeldTypes.RUN
        
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
                return True, MeldTypes.RUN
            
            if ruleset.ace_wrap_around and has_king:
    
                low_indices = [index for index in indices if index <5]
                high_indices = [index for index in indices if index >= 10]
                    
                if len(low_indices) > 0 and len(high_indices) > 0:
                    low_span = max(low_indices) - min(low_indices) + 1
                    high_span = max(high_indices) - min(high_indices) + 1
                        
                    total_gaps = (low_span - len(low_indices)) + (high_span - len(high_indices))
                    if total_gaps <= len(wilds):
                        return True, MeldTypes.RUN
                
        return False, "invalid run"
    
    
    @staticmethod
    def validate_meld(meld, ruleset):
        if meld.meld_type == MeldTypes.SET:
            return Validator.validate_set(meld, ruleset)
    
        elif meld.meld_type == MeldTypes.RUN:
            return Validator.validate_run(meld, ruleset)
    
        else:
            return False, "Invalid Meld Type"
    
    @staticmethod
    def validate_play_melds(stored_melds, has_melded, ruleset, required_score):
        if len(stored_melds) == 0:
            return False, "No Melds Stored"
        
        if not has_melded:
            total_score = 0
            for meld in stored_melds:
                total_score += meld.return_meld_value(ruleset)
            if total_score < required_score:
                return False, f"Minimum Score {ruleset.min_initial_meld_score}. Current Score {total_score}"
        return True, stored_melds
    
    @staticmethod
    def validate_lay_off(card, meld, ruleset):
        test_cards = meld.cards + [card]
        
        valid, error_or_meld_type = Validator.validate_meld(test_cards, ruleset)
        
        if valid:
            return True, None
        return False, error_or_meld_type
    
    @staticmethod    
    def validate_discard(card, cards, has_drawn, drawn_from_discard, ruleset):
        if card not in cards:
            return False, "Card Not In Hand"
        
        if not has_drawn:
            return False, "Not Drawn a Card"
        
        if ruleset.prevent_discard_same_card and drawn_from_discard == card:
            return False, "Can't Discard Card Immedietly Drawn From Discard Pile"
        
        return True, None
    
    @staticmethod
    def validate_draw(deck, has_drawn):
        if deck.is_empty():
            return False, "Deck is Empty"
        if has_drawn:
            return False, "Player has Drawn"
        
        return True, None
    
    @staticmethod
    def validate_draw_discard(card, discard, has_drawn, has_melded, ruleset):
        if discard.is_empty():
            return False, "Discard Pile is Empty"
        if has_drawn:
            return False, "Player has Drawn"
        if card not in discard.cards:
            return False, "Card isn't in Discard Pile"
        
        if ruleset.require_melding_to_draw_from_disc and not has_melded:
            return False, "Melding Required to Draw From Discard Pile"
        
        return True, None