# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 11:01:04 2026

@author: Faisal
"""

from game_logic.validator import Validator
from game_logic.meld import Meld

class Player:
    def __init__(self, player_id, name, hand):
        self.player_id = player_id
        self.name = name
        self.hand = hand
        self.curent_stored_melds = []
        self.completed_stored_melds = []
        self.score = 0
        self.has_melded = False
        self.has_drawn = False
        self.drawn_from_discard = None
    
    def store_meld(self, cards, ruleset):
        
        is_valid, meld_type = Validator.validate_meld(cards, ruleset)
        
        if not is_valid:
            return is_valid, meld_type
        
        meld = Meld(cards, meld_type, ruleset)
        
        self.current_stored_melds.append(meld)
        return True, meld

    def reset_current_stored_melds(self):    
        self.curent_stored_melds = []

    def return_stored_melds_score(self, ruleset):
        score = 0
        for meld in self.current_stored_melds:
            score += meld.return_meld_value(ruleset)
        
        return score
    
    def lay_off_card(self, card, meld, ruleset):
        
        valid, error = Validator.validate_lay_off(card, meld, ruleset)
        if valid:
            self.hand.remove_card(card)
        else:
            return valid, error
        
    
    def add_to_score(self, ruleset, points):
        if ruleset.scoring_method == 'negative':
            self.score += points
        else:
            self.score -= points
    
    
    def reset_player(self):
        self.hand.cards = []
        self.completed_stored_melds = []
        self.current_stored_melds = []
        self.score = 0
        self.has_melded = False
        self.has_drawn = False
        self.has_drawn_from_discard = False