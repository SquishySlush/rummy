from game_logic.utils import sort_rank, Suit


class Hand:
    """
    Represents a player's hand of cards.

    The hand stores both:
    - all cards currently held by the player
    - any cards currently selected for actions such as meld building

    It also provides utility methods for sorting, swapping, selecting,
    and calculating the total deadwood score of the hand.
    """

    def __init__(self):
        """
        Initialise an empty hand.

        Attributes:
            cards (list[Card]): All cards currently in the player's hand.
            selected_cards (list[Card]): Cards currently selected by the player.
        """
        self.cards = []
        self.selected_cards = []

    def __repr__(self):
        """
        Return a readable string representation of the hand.

        If cards have been selected, they are shown separately beneath the
        main hand contents. This is mainly useful for debugging and testing.

        Returns:
            str: A formatted string showing the hand contents.
        """
        card_strings = [str(card) for card in self.cards]

        if len(self.selected_cards) > 0:
            selected_card_strings = [str(card) for card in self.selected_cards]
            return ', '.join(card_strings) + "\nSelected Cards: " + ', '.join(selected_card_strings)

        return ', '.join(card_strings)

    def add_card(self, card):
        """
        Add a card to the player's hand.

        Args:
            card (Card): The card to add.
        """
        self.cards.append(card)

    def remove_card(self, card):
        """
        Remove a card from the player's hand.

        Args:
            card (Card): The card to remove.
        """
        self.cards.remove(card)

    def select_card(self, card):
        """
        Mark a card as selected.

        Selected cards are stored separately so that the player can build
        melds or perform actions without immediately changing the hand.

        Args:
            card (Card): The card to select.
        """
        if card not in self.selected_cards:
            self.selected_cards.append(card)

    def deselect_card(self, card):
        """
        Remove a card from the selected cards list.

        Args:
            card (Card): The card to deselect.
        """
        if card in self.selected_cards:
            self.selected_cards.remove(card)

    def deselect_all(self):
        """
        Clear all currently selected cards.
        """
        self.selected_cards = []

    def sort_by_rank(self):
        """
        Sort the hand by rank.

        The sorting logic is delegated to the shared sort_rank utility
        function so that card ordering is consistent across the program.
        """
        self.cards = sort_rank(self.cards)

    def sort_by_suit(self):
        """
        Sort the hand by suit, then by rank within each suit.

        This groups cards by suit first, then sorts each suit group by rank.
        """
        self.cards = self._sort_suit(self.cards)

    def swap_card(self, card1, card2):
        """
        Swap the positions of two cards in the hand.

        This may be useful for manual card ordering in future UI features.

        Args:
            card1 (Card): The first card to swap.
            card2 (Card): The second card to swap.
        """
        index1 = self.cards.index(card1)
        index2 = self.cards.index(card2)

        self.cards[index1], self.cards[index2] = self.cards[index2], self.cards[index1]

    def _sort_suit(self, items):
        """
        Sort a list of cards by suit, then by rank.

        Cards are first split into separate suit groups, then each group is
        sorted by rank before the full list is recombined.

        Args:
            items (list[Card]): The cards to sort.

        Returns:
            list[Card]: A new list of cards sorted by suit then rank.
        """


        #Splits the cards into lists, each containing one suit
        items_hearts = []
        items_clubs = []
        items_diamonds = []
        items_spades = []

        for card in items:
            if card.suit == Suit.Hearts:
                items_hearts.append(card)
            elif card.suit.value == Suit.Clubs:
                items_clubs.append(card)
            elif card.suit.value == Suit.Diamonds:
                items_diamonds.append(card)
            elif card.suit.value == Suit.Spades:
                items_spades.append(card)


        #Sorts each list of cards individually, before adding them together
        return (
            sort_rank(items_hearts)
            + sort_rank(items_clubs)
            + sort_rank(items_diamonds)
            + sort_rank(items_spades)
        )

    def is_empty(self):
        """
        Check whether the hand contains any cards.

        Returns:
            bool: True if the hand is empty, otherwise False.
        """
        return len(self.cards) == 0

    def calculate_deadwood(self, ruleset):
        """
        Calculate the deadwood score of the hand.

        Wild cards use the wildcard deadwood value from the ruleset.
        All other cards use their standard deadwood value.

        Args:
            ruleset (Ruleset): The active ruleset used for scoring.

        Returns:
            int: The total deadwood score of the hand.
        """
        deadwood_score = 0

        for card in self.cards:
            if ruleset.is_wild(card):
                deadwood_score += ruleset.wild_deadwood_score
            else:
                deadwood_score += card.return_value()

        return deadwood_score