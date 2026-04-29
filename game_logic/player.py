from game_logic.validator import Validator
from game_logic.meld import Meld


class Player:
    """
    Represent a player in the game.

    This class stores the player's identity, hand, score, and any melds or
    cards they are currently working with during their turn.

    Attributes:
        user_id: A unique identifier for the player.
        name (str): The player's name.
        hand: The player's hand object.
        current_stored_melds (list): Melds created during the current turn
            that are not yet fully committed.
        completed_stored_melds (list): Melds that have been completed and stored.
        stored_cards (list): Cards currently selected for creating a meld.
        ready (bool): Whether the player is ready to begin.
        score (int): The player's current score.
        has_melded (bool): Whether the player has made their opening meld.
        has_drawn (bool): Whether the player has drawn a card this turn.
        drawn_from_discard: Stores whether or what was drawn from the discard pile.
    """

    def __init__(self, user_id, name, hand):
        """
        Initialise a Player object.

        Args:
            user_id: A unique identifier for the player.
            name (str): The player's name.
            hand: The player's hand object.
        """
        self.user_id = user_id
        self.name = name
        self.hand = hand
        self.current_stored_melds = []
        self.completed_stored_melds = []
        self.stored_cards = []
        self.ready = False
        self.score = 0
        self.has_melded = False
        self.has_drawn = False
        self.drawn_from_discard = None

    def store_meld(self, ruleset):
        """
        Validate the currently stored cards and create a meld if valid.

        The selected stored cards are checked using the validator. If valid,
        a Meld object is created and added to the player's current stored melds.

        Args:
            ruleset: The active ruleset used to validate the meld.

        Returns:
            tuple:
                - (False, meld_type) if the cards do not form a valid meld.
                - (True, meld) if the meld is created successfully.
        """
        is_valid, meld_type = Validator.validate_meld(self.stored_cards, ruleset)

        if not is_valid:
            return False, meld_type

        meld = Meld(self.stored_cards, meld_type, ruleset)
        self.current_stored_melds.append(meld)

        # Clear all selected cards after successfully storing the meld.
        self.deselect_all()
        return True, meld

    def select_card(self, card):
        """
        Select a card from the player's hand.

        Args:
            card: The card to select.
        """
        self.hand.select_card(card)

    def deselect_card(self, card):
        """
        Deselect a card from the player's hand.

        Args:
            card: The card to deselect.
        """
        self.hand.deselect_card(card)

    def deselect_all(self):
        """
        Deselect all currently selected cards in the player's hand.
        """
        self.hand.deselect_all()

    def reset_current_stored_melds(self):
        """
        Clear all melds currently stored for this turn.
        """
        self.current_stored_melds = []

    def return_stored_melds_score(self, ruleset):
        """
        Calculate the total score of the player's current stored melds.

        Args:
            ruleset: The active ruleset used to score melds.

        Returns:
            int: The combined score of all current stored melds.
        """
        score = 0
        for meld in self.current_stored_melds:
            score += meld.return_meld_value(ruleset)

        return score

    def sort_rank(self):
        """
        Sort the player's hand by rank.
        """
        self.hand = self.hand.sort_by_rank()

    def sort_suit(self):
        """
        Sort the player's hand by suit.
        """
        self.hand = self.hand.sort_by_suit()

    def add_to_score(self, ruleset, points):
        """
        Update the player's score according to the scoring method.

        In negative scoring, points are added. Otherwise, points are subtracted.

        Args:
            ruleset: The active ruleset controlling score behaviour.
            points (int): The number of points to apply.
        """
        if ruleset.scoring_method == 'negative':
            self.score += points
        else:
            self.score -= points

    def get_stored_cards(self):
        """
        Return the cards currently stored by the player.

        Returns:
            list: The player's stored cards.
        """
        return self.stored_cards

    def reset_player(self):
        """
        Reset the player's game state for a new round or game.

        This clears the player's hand, stored melds, score, and turn-related
        status flags.
        """
        self.hand.cards = []
        self.completed_stored_melds = []
        self.current_stored_melds = []
        self.score = 0
        self.has_melded = False
        self.has_drawn = False
        self.drawn_from_discard = False
    
    def add_card(self, card):
        """
        Abstraction of the add_card method from the hand class.

        Args:
            card: card object to add to the player's hand.
        """
        self.hand.add_card(card)