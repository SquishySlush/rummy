# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 08:02:13 2026

@author: Faisal
"""


class Ruleset:
    def __init__(self, config=None):
        config = config or {}
        
        self.allow_sets = config.get('allow_sets', True)
        self.allow_runs = config.get('allow_runs', True)
        
        self.min_meld_size = config.get('min_meld_size', 3)
        self.max_meld_size_set = config.get('max_meld_size_set', 4)
        self.max_meld_size_run = config.get('max_meld_size_run', None)
        
        self.wilds = config.get('wilds', ['Joker'])
        self.num_wilds = config.get('num_wilds', [0])
        
        self.scoring_method = config.get('scoring_method', 'negative')
        
        self.ace_high = config.get('ace_high', False)
        self.ace_both = config.get('ace_both',  True)
        
    def is_wild(self, card):
        if card.rank in self.wilds:
            return True
        else:
            return False
    
    def to_dict(self):
        return {'allow_sets' : self.allow_sets,
                'allow_runs' : self.allow_runs,
                'min_meld_size' : self.min_meld_size,
                'max_meld_size_set' : self.max_meld_size_set,
                'max_meld_size_run' : self.max_meld_size_run,
                'wilds' : self.wilds,
                'num_wilds' : self.num_wilds,
                'scoring_method' : self.scoring_method,
                'ace_high' : self.ace_high,
                'ace_both' : self.ace_both}
    
        
        