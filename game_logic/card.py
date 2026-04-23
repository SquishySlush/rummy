from game_logic.utils import Suit, rank_index, rank_score
import json

class Card:
    def __init__(self, rank, suit, ruleset):
        """
        Initialises the card object, validating it against the known ranks known.
        Wild cards are validated differently than normal cards, as they do not require a suit.

        Args:
            rank (string): rank of the card, e.g. "Ace", or "8".
            suit (enum): suit of the card as a Suit enum value,
                Can be None for wildcards.
            ruleset (ruleset object): fcurrent ruleset, used for general validation.

        Returns:
            ValueError: If the rank is not valid
            ValueError: If  a non-wild card has an invalid suit.
        """

        wild_ranks = [wild[0] for wild in ruleset.wilds]

        if rank not in rank_index and rank not in wild_ranks:
        #A card must be either a standard rank or a wild rank.

            raise ValueError(f"{rank} is not a valid rank")
        
        if rank not in ruleset.wilds:
        #Non-wild cards must have a valid suit

            if suit not in Suit:
            #Checks if suit is a valid suit enum

                raise ValueError(f"{suit} is not a valid suit")

                
        self.rank = rank
        self.suit = suit
        self.ruleset = ruleset


        # Standard cards have an index used for ordering and run validation.
        # Wild cards do not have a fixed numeric index.
        if rank in rank_index:
            self.index = int(rank_index[rank]) 
        else:
            self.index = None 

    def return_rank_index(self):
        """
        Returns the index of the rank of the card object, used for run validation

        
        Returns:
            Integer: index of rank
        """
        return int(rank_index[self.rank])
    
    def __repr__(self):
        """
        Returns a readable string representation for a card.

        Useful for debugging and testing,
        so that a card object can be printed in a human readable form.
        
        Returns:
            String: Rank of Suits, e.g. "King of Clubs"
        """
        if self.suit is None:
            return f"{self.rank}"
        return f"{self.rank} of {self.suit.name}"    
    def __eq__(self, other):
        """
        Defines the equality of two card objects.
        Two cards are considered equal if they have the same rank and same suit

        Args:
            other (card object): The other card object being compared to.
        
        Returns:
            Boolean: True if equal, otherwise is false
        """


        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def return_value(self):
        """
        Returns the default value of a card, used for deadwood calculations.
        
        Returns:
            Integer: Default Rank Value
        """

        if  self.ruleset.is_wild(self):
            return self.ruleset.wild_deadwood_socre
        else:
            return rank_score[self.rank]
    
    def to_dict(self):
        """
        Converts the card into a dictionary representation

        Used for serialising any move used so that card data can be sent
        ti the frontend or written to a file


        Returns:
            Dictionary: rank and suit key value pairs.
        """

        return {
            'rank': self.rank,
            'suit': self.suit.name if self.suit is not None else None
            }
    
    @classmethod
    def from_dict(cls, data, ruleset):
        """
        Classmethod, creates a card object from a dictionary,
        requires the same format as to_dict method.

        Args:
            Dictionayr: rank and suit key value pairs.
        
        Returns:
            Card object.
        """
        rank = data['rank']
        suit = Suit[data.get('suit')]
        return cls(rank, suit, ruleset)
    
    def to_json_file(self, filename):
        """
        Writes the card data to JSON file

        Args:
            self, filename
        
        Returns:
            JSON file
        """
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

