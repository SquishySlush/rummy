# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 08:02:13 2026

@author: Faisal
"""
class Ruleset:
    def __init__(self, config=None):
        config = config or {}
        
        #Are sets or runs allows, or both. At least one should be enabled, otherwise the game is imposible to finish.
        self.allow_sets = config.get('allow_sets', True)
        self.allow_runs = config.get('allow_runs', True)
        
        #Meld size limitations.
        self.min_meld_size = config.get('min_meld_size', 3)
        self.max_meld_size_set = config.get('max_meld_size_set', 4)
        self.max_meld_size_run = config.get('max_meld_size_run', None)
        
        #What wild cards exist? Created as a list, and any card that is in both this list and the dictionary should be removed from the dictionary. Wild cards can have  suits or ranks, but it doesnt matter.
        self.wilds = config.get('wilds', ['Joker'])
        self.num_wilds = config.get('num_wilds', [0])
        
        #Scoring method. Negative scoring gives to winner negative points, and the loser gets points based off of the cards in their hands
        self.scoring_method = config.get('scoring_method', 'negative')
        
        #Ace settings, for ace low, high,, both, and wrap around. Wrap around aces can go King, Ace, 2.
        self.ace_low = config.get('ace_high', False)
        self.ace_high = config.get('ace_high', False)
        self.ace_both = config.get('ace_both',  True)
        self.ace_wrap_around = config.get('wrap_around', False)
        self.ace_high_score = config.get('ace_high_score', 10)
    
    def is_wild(self, card):
        if card.rank in self.wilds:
            return True
        
    
    def to_dict(self): #Exports the ruleset to a dictionary, so it can be saved and loaded.
        return {'allow_sets' : self.allow_sets,
                'allow_runs' : self.allow_runs,
                'min_meld_size' : self.min_meld_size,
                'max_meld_size_set' : self.max_meld_size_set,
                'max_meld_size_run' : self.max_meld_size_run,
                'wilds' : self.wilds,
                'num_wilds' : self.num_wilds,
                'scoring_method' : self.scoring_method,
                'ace_high' : self.ace_high,
                'ace_both' : self.ace_both,
                'ace_high_score' : self.ace_high_score}
    
        
        