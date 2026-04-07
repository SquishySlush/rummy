# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:35:42 2026

@author: Faisal Mustafa
"""

from game_logic.card import Card
from game_logic.hand import Hand
from game_logic.deck import Deck
from game_logic.meld import Meld
from game_logic.discard_pile import Discard_pile
from game_logic.player import Player
from game_logic.ruleset import Ruleset
from game_logic.validator import Validator
from game_logic.utils import Suit


ruleset = Ruleset()

card = Card("King", Suit.Clubs, ruleset)

if card.suit == Suit.Clubs:
    print(card)