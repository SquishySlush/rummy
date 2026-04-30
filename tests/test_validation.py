from game_logic.card import Card
from game_logic.validator import Validator
from game_logic.utils import Suit, MeldTypes
from game_logic.ruleset import Ruleset
from game_logic.meld import Meld, MeldTypes
from game_logic.player import Player
from game_logic.hand import Hand
from game_logic.deck import Deck
from game_logic.discard_pile import DiscardPile

ruleset = Ruleset()


#Meld Validation Tests
def test_valid_set():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Hearts, ruleset)
    c3 = Card("7", Suit.Diamonds, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    assert valid is True, f"Expected valid set, got: {error}"

def test_set_with_wild():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Spades, ruleset)
    c3 = Card("Joker", None, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    assert valid is True, f"Expected valid set, got: {error}"

def test_set_duplicate():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Clubs, ruleset)
    c3 = Card("7", Suit.Diamonds, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid set due to duplicate cards"

def test_set_small():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Hearts, ruleset)

    cards = [c1, c2]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "expected invalid set due to not enough cards."

def test_set_mixed_rank():
    c1 = Card("6", Suit.Clubs, ruleset)
    c2 = Card("7", Suit.Spades, ruleset)
    c3 = Card("7", Suit.Diamonds, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid set due to mixed rank"

def test_valid_run():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("9", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    assert valid is True, f"Expected valid run, got: {error}"

def test_run_duplicate():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("8", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid run, due to duplicate cards"

def test_run_with_wild():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("Joker", None, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    assert valid is True, f"Expected valid run, got: {error}"

def test_run_mixed_suits():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Hearts, ruleset)
    c3 = Card("9", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid run due to mixed suits"

def test_run_with_gaps():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Hearts, ruleset)
    c3 = Card("10", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid run due to gaps"

def test_run_with_wild_inbetween():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("9", Suit.Clubs, ruleset)
    c3 = Card("Joker", None, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    assert valid is True, f"Expected valid run, got: {error}"

def test_run_with_wild_with_gaps():
    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("Joker", Suit.Hearts, ruleset)
    c3 = Card("10", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    valid, error = Validator.validate_meld(cards, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid run due to gaps"

def test_validation_under_100ms():
    import time

    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("9", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    start = time.perf_counter()
    Validator.validate_meld(cards, ruleset)
    end = time.perf_counter()

    t= end-start

    print(t)

    assert t < 0.1, "Validation takes longet than 100ms"


#Lay Off Validation Tests
def test_lay_off_run():

    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("9", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    meld = Meld(cards, MeldTypes.RUN, ruleset)

    card = Card("10", Suit.Clubs, ruleset)

    valid, error = Validator.validate_lay_off(card, meld, ruleset)

    assert valid is True, f"Expected valid lay off, got {error}"

def test_lay_off_invalid_suit():

    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("9", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    meld = Meld(cards, MeldTypes.RUN, ruleset)

    card = Card("10", Suit.Spades, ruleset)

    valid, error = Validator.validate_lay_off(card, meld, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid lay off due to invalid suit"

def test_lay_off_gaps():

    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("9", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    meld = Meld(cards, MeldTypes.RUN, ruleset)

    card = Card("Jack", Suit.Clubs, ruleset)

    valid, error = Validator.validate_lay_off(card, meld, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid lay off due to gaps"

def test_lay_off_duplicate():

    c1 = Card("7", Suit.Clubs, ruleset)
    c2 = Card("8", Suit.Clubs, ruleset)
    c3 = Card("9", Suit.Clubs, ruleset)

    cards = [c1, c2, c3]

    meld = Meld(cards, MeldTypes.RUN, ruleset)

    card = Card("9", Suit.Clubs, ruleset)

    valid, error = Validator.validate_lay_off(card, meld, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid lay off due to gaps"

#Draw Validation:
def test_draw():

    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    
    deck = Deck(ruleset)

    valid, error = Validator.validate_draw(deck, p1.has_drawn)

    assert valid is True, f"Expected valid draw, got {error}"

def test_draw_has_drawn():

    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    p1.has_drawn = True

    deck = Deck(ruleset)

    valid, error = Validator.validate_draw(deck, p1.has_drawn)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid draw due to player having drawn"

def test_draw_empty_deck():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)

    deck = Deck(ruleset)
    deck.cards = []

    valid, error = Validator.validate_draw(deck, p1.has_drawn)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid draw due to deck being empty"

def test_draw_from_disc():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    p1.has_melded = True

    discard_pile = DiscardPile()
    discard_pile.push(Card("7", Suit.Clubs, ruleset))

    valid, error = Validator.validate_draw_discard(
        discard_pile.peek(),
        discard_pile,
        p1.has_drawn,
        p1.has_melded,
        ruleset
    )

    assert valid is True, f"Expected valid draw, got {error}"

def test_draw_from_disc_not_melded():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    p1.has_melded = False

    discard_pile = DiscardPile()
    c1 = Card("7", Suit.Clubs, ruleset)
    discard_pile.push(c1)
    valid, error = Validator.validate_draw_discard(discard_pile.peek(), discard_pile, p1.has_drawn, p1.has_melded, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid draw due to player not having melded"

def test_draw_from_empty_disc():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    p1.has_melded = True

    discard_pile = DiscardPile()
    valid, error = Validator.validate_draw_discard(discard_pile.peek, discard_pile, p1.has_drawn, p1.has_melded, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid draw due to player not having melded"

#Discard Validation
def test_discard():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    p1.has_drawn = True

    c1 = Card("7", Suit.Clubs, ruleset)
    p1.add_card(c1)
    valid, error = Validator.validate_discard(c1, p1.hand.cards, p1.has_drawn, p1.drawn_from_discard, ruleset)

    assert valid is True, f"Expected valid discard, got {error}"

def test_discard_not_drawn():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)

    c1 = Card("7", Suit.Clubs, ruleset)
    p1.add_card(c1)
    valid, error = Validator.validate_discard(c1, p1.hand.cards, p1.has_drawn, p1.drawn_from_discard, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid discard due to not having drawn card"

def test_discard_same_card():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    p1.has_drawn = True

    c1 = Card("7", Suit.Clubs, ruleset)
    p1.add_card(c1)
    p1.drawn_from_discard = c1 #type: ignore
    valid, error = Validator.validate_discard(c1, p1.hand.cards, p1.has_drawn, p1.drawn_from_discard, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid discard due to discarding the card just drawn from the discard pile."

def test_discard_not_in_hand():
    h = Hand()

    p1 = Player("1", "Test_User_1", h)
    p1.has_drawn = True

    c1 = Card("7", Suit.Clubs, ruleset)
    valid, error = Validator.validate_discard(c1, p1.hand.cards, p1.has_drawn, p1.drawn_from_discard, ruleset)

    print(f"Result: {valid}, Message: {error}")

    assert valid is False, "Expected invalid discard due to discarding the card just drawn from the discard pile."