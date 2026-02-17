# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 12:23:46 2026

@author: Faisal
"""

from game_logic.card import Card, Suit, rank_index
from game_logic.hand import Hand
import random

inverted_rank_index = {v: k for k, v in rank_index.items()} #For creating an inverted list, such that a rng can select any rank.

hand = Hand()

for  i in range(14): #Testing creating random cards
    random_index = random.randint(0, 12)
    random_suit = random.randint(0, 3)
    card =  Card(inverted_rank_index[random_index], Suit(random_suit), 0)
    hand.add_card(card) #Testing adding them to hand




print(hand) #Hand before sorting

hand.sort_by_rank()
print( "\n \n", hand)


hand.sort_by_suit()
print("\n \n", hand)


    



