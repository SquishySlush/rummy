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
        self.max_meld_size_run = None
        
        self.wilds = config.get('wilds', 'Joker')
        self.num_wilds = config.get('num_wilds', 0)
        