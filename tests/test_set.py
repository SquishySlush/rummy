from game_logic.validator import Validator
from game_logic.card import Card
from game_logic.utils import Suit, MeldTypes
from game_logic.ruleset import Ruleset

ruleset = Ruleset()

def test_valid_set():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Hearts, ruleset)
    c3 = Card("7", Suit.Diamonds, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    assert valid is True, f"Expected valid set, got: {error}"

def test_valid_set_duplicate():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Clubs, ruleset)
    c3 = Card("7", Suit.Diamonds, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    assert valid is True, f"Expected valid set, got: {error}"

def test_valid_set_duplicate():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Clubs, ruleset)
    c3 = Card("7", Suit.Diamonds, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Duplicate suits should make set invalid"