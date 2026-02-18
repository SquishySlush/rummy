# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 10:02:52 2026

@author: Faisal
"""
from game_logic.utils import rank_index, Suit
from game_logic.card import Card
import random

class Deck:
    def __init__(self, num_jokers):
        self.cards = []
        self.num_jokers =  int(num_jokers)
        for  rank in rank_index:
            for suit in Suit:
                self.cards.append(Card(rank, suit, 0))
        for i in range(num_jokers):
            self.cards.append(Card("Joker", "", 1))
    
    def shuffle(self):
        result = []
        for i in range(len(self.cards)):
            roll = random.randint(0, len(self.cards)-1)
            result.append(self.cards[roll])
            self.cards.remove(self.cards[roll])
        self.cards  = result
    
    def draw(self):
        return self.cards.pop()
    
    def size(self):
        return len(self.cards)
    
    def empty_check(self):
        if len(self.cards) == 0:
            return
    
    def add_cards(self, cards):
        self.cards.append(cards)
    

    


