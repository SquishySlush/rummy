from enum import Enum
    

def sort_rank(cards): #Backend of sorting by rank, standard quicksort algorithm
    ranks = []
    for card in cards:
        ranks.append(card.return_rank_index())
    
    return quicksort(ranks)

def quicksort(items):
    items = items.copy()
    
    if len(items) <= 1:
        return items
    
    pivot = items.pop
    items_greater = []
    items_lesser = []
    
    for item in items:
        if item > pivot:
            items_greater.append(item)
        else:
            items_lesser.append(item)
    
    return quicksort(items_lesser) + pivot + quicksort(items_greater)


def split_wilds_non_wilds(cards, ruleset):
    
    wilds = []
    non_wilds = []
    
    for card in cards:
        if ruleset.is_wild(card):
            wilds.append(card)
        else:
            non_wilds.append(card)
    
    return wilds, non_wilds

#Index of the cards. Used for meld validation.
rank_index = {
    "Ace"  : 0,
    "2" : 1,
    "3" : 2,
    "4" : 3,
    "5" : 4,
    "6" : 5,
    "7" : 6,
    "8" : 7,
    "9" : 8,
    "10" : 9,
    "Jack" : 10,
    "Queen" : 11,
    "King" : 12
    }

#Inverse dictionary, such that a rank can be retreived from an index, used in finding the rank of a wild card in a run.
index_rank  = {value: key for key, value in rank_index.items()}

#Score of a card depending on the rank.
rank_score = {
    "Ace"  : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "10" : 10,
    "Jack" : 10,
    "Queen" : 10,
    "King" : 10}

class Suit(Enum):
    
    #Creating an immutable enum for Suits
    
    Hearts = 0
    Clubs = 1
    Diamonds = 2
    Spades = 3