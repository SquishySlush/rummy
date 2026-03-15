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
        self.stored_melds = []
        self.score = 0
        self.has_melded = False
        
    def store_meld(self, cards, ruleset):
        
        is_valid, meld_type = Validator.validate_meld(cards, ruleset)
        
        if not is_valid:
            return False, "Invalid Meld"
        
        meld = Meld(cards, meld_type, ruleset)
        
        self.stored_melds.append(meld)
    
    def clear_stored_melds(self):
        self.stored_melds = []
    
    def play_stored_melds(self, ruleset, gamestate):
        
        if len(self.stored_melds) == 0:
            return False, "No Melds Stored"
        
        total_meld_score = 0
        for meld in self.stored_melds:
            total_meld_score += meld.return_meld_value(ruleset)
        
        if not self.has_melded:
            required_score = gamestate.return_meld_requirement()
            if total_meld_score < required_score:
                return False, f"Minimum score {required_score}. Current Score {total_meld_score}"
        
        for meld in self.stored_melds:
            for card in meld.cards:
                self.hand.remove_card(card)
        
        melds_to_play = self.stored_melds.copy()
        
        self.clear_stored_melds()
        self.has_melded = True
        
        return True, melds_to_play
    
    def return_stored_melds_score(self, ruleset):
        score = 0
        for meld in self.stored_melds:
            score += meld.return_meld_value(ruleset)
        
        return score
    
    def lay_off_card(self, card, meld, ruleset):
        test_cards = meld.cards + [card]
        
        valid, meld_type = Validator.validate_meld(test_cards, ruleset)
        
        if valid:
            meld.add_card(card)
            self.hand.remove_card(card)
            return True, "Card Added"
        else:
            return False, "Card doesn't Fit in Meld"
    
    def calculate_deadwood(self, ruleset):
        deadwood_score = 0
        for card in self.hand.cards:
            if ruleset.is_wild(card):
                deadwood_score += ruleset.wild_deadwood_score
            else:
                deadwood_score += card.return_value()
        
        return deadwood_score
    
    def add_to_score(self, ruleset, points):
        if ruleset.scoring_method == 'negative':
            self.score += points
        else:
            self.score -= points
    
    def reset_player(self):
        self.hand.cards = []
        self.has_melded = False
        self.stored_melds = []
        self.score = 0