# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 08:02:13 2026

@author: Faisal
"""

import json


class Ruleset:
    def __init__(self, config=None):
        config = config or {}
        
        # Are sets or runs allows, or both. 
        # At least one should be enabled, otherwise 
        # the game is imposible to finish.
        self.allow_sets = self._get_validated(
            config, 
            'allow_sets', 
            True, 
            bool)
        
        self.allow_runs = self._get_validated(
            config, 
            'allow_runs', 
            True, 
            bool)      
        #Meld size limitations.
        self.max_meld_size_run = self._get_validated(
            config, 
            'max_meld_size_run', 
            None, 
            int,
            None,
            1,
            None)
        
        self.min_initial_meld_score = self._get_validated(
            config, 
            'min_initial_meld_score', 
            0, 
            int,
            None,
            0,
            None)
        
        self.initial_meld_increment = self._get_validated(
            config, 
            'initial_meld_increment', 
            False, 
            bool)
        #What wild cards exist? Created as a list, and any card that is in both this list and the dictionary should be removed from the dictionary. Wild cards can have  suits or ranks, but it doesnt matter.
        self.wilds = self._get_validated(
            config, 
            'wilds', 
            [("Joker", 0)], 
            list)
        
        self.wild_deadwood_score = self._get_validated(
            config, 
            'wild_deadwood_score', 
            25,
            int,
            None,
            0,
            None)
        #Scoring method. Negative scoring gives to winner negative points, and the loser gets points based off of the cards in their hands
        self.scoring_method = self._get_validated(
            config, 
            'scoring_method', 
            'negative', 
            str,
            ['negative', 'positve'])       
        #Ace settings, for ace low, high,, both, and wrap around. Wrap around aces can go King, Ace, 2.
        self.ace_low = self._get_validated(
            config, 
            'ace_low', 
            False, 
            bool)
        
        self.ace_high = self._get_validated(
            config, 
            'ace_high', 
            False, 
            bool)
        
        self.ace_both = self._get_validated(
            config, 
            'ace_both', 
            True, 
            bool)
        
        self.ace_wrap_around = self._get_validated(
            config, 
            'wrap_around', 
            False, 
            bool)
        
        self.ace_high_score = self._get_validated(
            config, 
            'ace_high_score', 
            10, 
            int, 
            None, 
            1)     
        
        self.initial_hand_size = self._get_validated(
            config, 
            'initial_hand_size', 
            14, 
            int,
            None, 
            1)
        
        self.min_meld_size = self._get_validated(
            config, 
            'min_meld_size', 
            3, 
            int,
            None,
            1,
            self.initial_hand_size)
        
        self.max_meld_size_set = self._get_validated(
            config, 
            'max_meld_size_set', 
            4, 
            int,
            None,
            1,
            self.initial_hand_size)
        
        self.num_decks = self._get_validated(
            config, 
            'num_decks', 
            2, 
            int, 
            None, 
            1)
        
        self.require_melding_to_draw_from_disc = self._get_validated(
            config, 
            'require_melding_to_draw_from_disc', 
            True, 
            bool)
        
        self.require_melding_to_lay_off = self._get_validated(
            config, 
            'require_melding_to_lay_off', 
            True, 
            bool)
        
        self.allow_wild_replacement = self._get_validated(
            config, 
            'allow_wild_replacement', 
            True, 
            bool)
        
        self.allow_wild_only_melds = self._get_validated(
            config, 
            'allow_wild_only_melds',
            False, 
            bool)
        
        self.prevent_discard_same_card = self._get_validated(
            config, 
            'prevent_discard_same_card', 
            True, 
            bool)
        
        self.points_for_winning = self._get_validated(
            config, 
            'points_for_winning', 
            25, 
            int)
        
        self.max_deck_shuffle = self._get_validated(
            config, 
            'max_deck_shuffle', 
            None, 
            int)
            
        self.winner_deadwood = self._get_validated(
            config, 
            'winner_deadwood', 
            25, 
            int)        
        
        self.max_players = self._get_validated(
            config,
            'max_players',
            4,
            int
        )

    def _get_validated(
            self, 
            config, 
            key, 
            default, 
            expected_type, 
            allowed_values=None, 
            min_value=None, 
            max_value=None):
        
        value = config.get(key, default)
        
        if value is not None and not isinstance(value, expected_type):
            return default
        if allowed_values is not None and value not in allowed_values:
            return default
        
        if min_value is not None and value < min_value:
            return default
        if max_value is not None and value > max_value:
            return default
        
        return value
        
    
    def is_wild(self, card):
        return any(card.rank == t[0] for t in self.wilds)

    def to_dict(self): #Exports the ruleset to a dictionary, so it can be saved and loaded.
        return {'allow_sets' : self.allow_sets,
                'allow_runs' : self.allow_runs,
                'min_meld_size' : self.min_meld_size,
                'max_meld_size_set' : self.max_meld_size_set,
                'max_meld_size_run' : self.max_meld_size_run,
                'min_initial_meld_score' : self.min_initial_meld_score,
                'initial_meld_increment' : self.initial_meld_increment,
                'initial_hand_size' : self.initial_hand_size,
                'num_decks' : self.num_decks,
                'wilds' : self.wilds,
                'scoring_method' : self.scoring_method,
                'ace_high' : self.ace_high,
                'ace_both' : self.ace_both,
                'ace_high_score' : self.ace_high_score}
    
    #Writes dictionary to json file
    def to_json_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)
    
    #Retrieves dictionary from json file, returning cls(data)
    @classmethod
    def from_json_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls(data)
    
    @classmethod
    def from_dict(cls, dictionary):
        return cls(dictionary)