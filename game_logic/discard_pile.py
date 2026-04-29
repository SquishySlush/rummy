class DiscardPile:
    """
    Represents the discard pile used during gameplay.

    The discard pile stores cards that have been discarded by players.
    The top card may be viewed or drawn, while the rest of the pile can
    be split off and reshuffled back into the deck when required.
    """

    def __init__(self):
        """
        Initialise an empty discard pile.
        """
        self.cards = []

    def __repr__(self):
        """
        Return a readable string representation of the discard pile.

        If the discard pile is empty, a message is returned instead.
        Otherwise, the top card is shown.

        Returns:
            str: A description of the top card, or a message if empty.
        """
        if self.is_empty():
            return "Empty discard pile"

        return f"Top card: {self.cards[-1]}"

    def push(self, card):
        """
        Add a card to the top of the discard pile.

        Args:
            card (Card): The card being discarded.
        """
        self.cards.append(card)

    def draw_top_card(self):
        """
        Remove and return the top card from the discard pile.

        Returns:
            tuple: (True, Card) if a card was successfully drawn,
                or (False, error_message) if the pile is empty.
        """
        if self.is_empty():
            return False, "Cannot draw from empty discard pile"

        return True, self.cards.pop()

    def split_discard_pile(self):
        """
        Remove all but the top card from the discard pile.

        This is used when the discard pile needs to be recycled back into
        the deck, while keeping the current top card visible.

        Returns:
            list[Card]: All cards except the top card.
        """

        if len(self.cards) <= 1:
            return []

        top_card = self.cards[-1]
        cards_to_reshuffle = self.cards[:-1]

        self.cards = [top_card]

        return cards_to_reshuffle

    def is_empty(self):
        """
        Check whether the discard pile is empty.

        Returns:
            bool: True if the discard pile contains no cards, otherwise False.
        """
        return len(self.cards) == 0

    def peek(self):
        """
        Return the top card of the discard pile without removing it.

        Returns:
            Card: The top card of the discard pile, None if pile is empty
        """
        if self.is_empty():
            return None
        return self.cards[-1]