from enum import Enum


def sort_rank(cards):
    """
    Return cards sorted by rank.

    Args:
        cards
    """
    return quicksort(cards, key=lambda card: card.return_rank_index())


def quicksort(items, key=lambda x: x):
    """
    Sort a list using quicksort with an optional key function.

    Args:
        items (list): Items to sort.
        key (function): Function to extract comparison value.

    Returns:
        list: Sorted list.
    """
    items = items.copy()

    if len(items) <= 1:
        return items

    pivot = items.pop()
    pivot_value = key(pivot)

    lesser = []
    greater = []

    for item in items:
        if key(item) > pivot_value:
            greater.append(item)
        else:
            lesser.append(item)

    return quicksort(lesser, key) + [pivot] + quicksort(greater, key)


def split_wilds_non_wilds(cards, ruleset):
    """
    Split a list of cards into wild and non-wild cards.

    Args:
        cards (list): The cards to split.
        ruleset: The active ruleset used to determine whether a card is wild.

    Returns:
        tuple: A tuple containing:
            - list: all wild cards
            - list: all non-wild cards
    """
    wilds = []
    non_wilds = []

    for card in cards:
        if ruleset.is_wild(card):
            wilds.append(card)
        else:
            non_wilds.append(card)

    return wilds, non_wilds


# Map each card rank to its index position.
# This is mainly used for meld validation and run checking.
rank_index = {
    "Ace": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "10": 9,
    "Jack": 10,
    "Queen": 11,
    "King": 12
}

# Reverse the rank_index dictionary so a rank name can be retrieved
# from its index. This is useful when assigning wild cards in runs.
index_rank = {value: key for key, value in rank_index.items()}

# Store the score value for each rank.
rank_score = {
    "Ace": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}


class Suit(Enum):
    """
    Represent the four card suits as an immutable enumeration.
    """
    Hearts = 0
    Clubs = 1
    Diamonds = 2
    Spades = 3


class Moves(Enum):
    """
    Represent the possible player actions in the game.

    Each enum value stores the move name used by the system.
    """
    Draw_Deck = "Draw_Deck"
    Draw_Discard = "Draw_Discard"
    Discard = "Discard"
    Store_Meld = "Store_Meld"
    Meld = "Meld"
    Store_Card = "Store_Card"
    Deselect_all = "Deselect_all"
    Lay_Off = "Lay_Off"
    Deck_Shuffle = "Deck_Shuffle"
    Sort_Rank = "Sort_Rank"
    Sort_Suit = "Sort_Suit"


class MeldTypes(Enum):
    """
    Represent the two possible meld types in the game.
    """
    RUN = "run"
    SET = "set"