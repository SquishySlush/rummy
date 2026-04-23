from game_logic.utils import rank_index, Suit
from game_logic.card import Card
import random

local_rank_index = rank_index.copy()

class Deck:
    
    """
    Represents a deck of playing cards used in the game.

    The deck is constructed based on the current ruleset, including:
    - number of standard decks
    - wildcard types and counts

    A seeded random number generator is used to ensure deterministic
    shuffling when required.
    """

    def __init__(self, ruleset, seed=None):
        """
        Initialise a deck of cards based on the provided ruleset.

        The deck consists of:
        - Standard cards (rank + suit combinations)
        - Wildcards (with no suit, depending on ruleset)

        A random seed is used to allow reproducible shuffling.

        Args:
            ruleset (Ruleset): The ruleset defining deck composition.
            seed (int, optional): Seed for deterministic randomness.
                If None, a secure random seed is generated.
        """


        if seed is None:
            #Generates a secure 32bit seed using OS random generator
            seed = random.SystemRandom().randint(0, 2**32 -1)

        self.cards = []
        self.seed = seed
        self.rng = random.Random(seed)
        
        wild_ranks = [wild[0] for wild in ruleset.wilds]

        #Creates all standard cards
        for deck in range(ruleset.num_decks):
            for rank in rank_index:
                if rank not in wild_ranks:
                    for suit in Suit:
                        self.cards.append(Card(rank, suit, ruleset))
                
        #Add wildcard cards to deck
        for wild, num_wild in ruleset.wilds:
            for i in range(num_wild):
                self.cards.append(Card(wild, None, ruleset))
    

    
    def shuffle(self):
        """
        Shuffles the deck using a Fisher-Yates style algorithm.
        
        Ensures an unbiased shuffle using the seeded random generator.
        """
        for i in range(len(self.cards) -1, 0, -1):
            roll = self.rng.randint(0, i)
            self.cards[i], self.cards[roll] = self.cards[roll], self.cards[i]    
    
    def peek(self):
        """
        Return the top card of the deck, without removing it.

        Returns:
            Card: top card of the deck
        """
        return self.cards[-1]
    
    def draw(self):
        """
        Remove and return the top card of the deck, simulating drawing a card.

        Returns:
            Card: The card removed from the  top of the deck.
        """
        return self.cards.pop()
    
    def size(self):
        """
        Returns the number of cards currently remaining in the deck.

        Returns:
            int: the number of cards in the deck
        """
        return len(self.cards)
    
    def empty_check(self):
        """
        Checks whether the deck is empty.

        Returns:
            bool: True if the deck contains no cards, otherwise False.
        """
        return self.size() == 0
    
    def add_cards(self, cards):
        """
        Add multiple cards to the deck.

        This is typically used when recycling cards from a discard pile
        back into the deck.

        Args:
            cards (list[Card]): A list of Card objects to add to the deck.
        """
        self.cards.extend(cards)

