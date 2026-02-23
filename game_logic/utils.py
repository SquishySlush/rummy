from enum import Enum

def sort_rank(items): #Backend of sorting by rank, standard quicksort algorithm
    if len(items) <= 1:
        return items
    pivot_card = items.pop()
    pivot_index = pivot_card.return_rank_index()
    items_greater = []
    items_lower = []
        
    for i in items:
        if i.return_rank_index() > pivot_index:
            items_greater.append(i)
        else:
            items_lower.append(i)
    return sort_rank(items_lower) + [pivot_card] + sort_rank(items_greater)

rank_index = { #Index of the cards. Used for meld validation and score.
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

index_rank  = {value: key for key, value in rank_index.items()}

wilds = [] #list of all wild cards



class Suit(Enum):
    
    #Creating an immutable enum for Suits
    
    Hearts = 0
    Clubs = 1
    Diamonds = 2
    Spades = 3