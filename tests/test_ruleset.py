from game_logic.card import Card
from game_logic.utils import Suit
from game_logic.ruleset import Ruleset
import json

def test_default_ruleset_loads():
    ruleset = Ruleset()

    assert ruleset.allow_sets is True
    assert ruleset.allow_runs is True
    assert ruleset.initial_hand_size > 0

def test_custom_rule():
    config = {
        "min_meld_size": 4,
        "num_decks": 3
    }

    ruleset = Ruleset(config)

    assert ruleset.min_meld_size == 4
    assert ruleset.num_decks == 3

def test_invalid_type_returns_default():
    config =  {
        "min_meld_size": "invalid"
    }

    ruleset =  Ruleset(config)

    assert ruleset.min_meld_size == 3 #Default meld size.

def test_min_value_enforced():
    config = {
        "num_decks": 0
    }

    ruleset = Ruleset(config)

    assert ruleset.num_decks == 2 #Default number of decks

def test_is_wild():
    ruleset = Ruleset({"wilds": [("Joker", 0)]})

    card = Card("Joker", Suit.Spades, ruleset)

    assert ruleset.is_wild(card) is True

def test_not_wild():
    ruleset = Ruleset()

    card = Card("7", Suit.Clubs, ruleset)

    assert ruleset.is_wild(card) is False

def test_to_dict():
    ruleset = Ruleset({"num_decks": 3})

    data = ruleset.to_dict()

    assert data["num_decks"] == 3

def test_from_dict():
    config = {"min_meld_size": 4}

    ruleset = Ruleset.from_dict(config)

    assert ruleset.min_meld_size == 4