from game_logic.utils import index_rank, Suit, rank_score, MeldTypes, split_wilds_non_wilds, quicksort


class Meld:
    """
    Represent a single meld in the rummy game.

    A meld can be either a set or a run. The class stores the cards in the meld,
    its type, and any wild card assignments needed to make the meld valid.

    Attributes:
        cards (list): The cards currently in the meld.
        meld_type: The type of meld, usually set or run.
        wild_assignments (dict): Maps each wild card to the card details it is
            representing in the meld.
    """

    def __init__(self, cards, meld_type, ruleset):
        """
        Initialise a Meld object.

        Args:
            cards (list): The cards that make up the meld.
            meld_type: The meld type, such as set or run.
            ruleset: The ruleset object controlling allowed meld behaviour.
        """
        self.cards = cards
        self.meld_type = meld_type
        self.wild_assignments = {}

        # Only assign wild cards if the meld type is allowed by the ruleset.
        if self.meld_type == MeldTypes.RUN:
            if ruleset.allow_runs:
                self._wild_assignment_run(ruleset)
        else:
            if ruleset.allow_sets:
                self._wild_assignment_set(ruleset)

    def __repr__(self):
        """
        Return a string representation of the meld.

        Returns:
            str: A comma-separated string of the cards in the meld.
        """
        card_strings = [str(card) for card in self.cards]
        return ",".join(card_strings)

    def _wild_assignment_run(self, ruleset):
        """
        Assign values to wild cards when the meld is a run.

        Wild cards are first used to fill gaps between non-wild cards.
        Any remaining wild cards are then assigned to extend the run,
        defaulting to the lower end.

        Args:
            ruleset: The active ruleset used to identify wild cards.
        """
        wilds, non_wilds = split_wilds_non_wilds(self.cards, ruleset)

        # Build and sort the rank indices of all non-wild cards.
        indices = []
        for card in non_wilds:
            indices.append(card.return_rank_index())

        indices = quicksort(indices)

        # Create the full expected range of indices across the run.
        range_indexes = range(indices[0], indices[-1] + 1)

        # Identify any missing ranks between the lowest and highest cards.
        missing_indices = []
        for index in range_indexes:
            if index not in indices:
                missing_indices.append(index)

        # Assign wild cards to fill missing ranks inside the run.
        assigned_wilds = []

        for wild, missing_index in zip(wilds, missing_indices):
            self.wild_assignments[wild] = {
                'score': rank_score[index_rank[missing_index]],
                'rank_index': missing_index,
                'rank': index_rank[missing_index],
                'suit': non_wilds[0].suit
            }
            assigned_wilds.append(wild)

        # Remove wild cards that have already been assigned.
        for wild in assigned_wilds:
            wilds.remove(wild)

        # Assign any remaining wild cards to extend the run downward.
        if len(wilds) > 0:
            for i, wild in enumerate(wilds):
                self.wild_assignments[wild] = {
                    'score': rank_score[index_rank[min(indices) - (len(wilds) - i)]],
                    'rank_index': min(indices) - (len(wilds) - i),
                    'rank': index_rank[min(indices) - (len(wilds) - i)],
                    'suit': non_wilds[0].suit
                }

    def _wild_assignment_set(self, ruleset):
        """
        Assign values to wild cards when the meld is a set.

        Wild cards take the same rank and score as the non-wild cards,
        and are assigned suits that are not already represented.

        Args:
            ruleset: The active ruleset used to identify wild cards.
        """
        wilds, non_wilds = split_wilds_non_wilds(self.cards, ruleset)

        # Collect the suits already present in the non-wild cards.
        non_wild_suits = []

        for card in non_wilds:
            non_wild_suits.append(card.suit)

        # Find suits not yet used in the set.
        missing_suits = []

        for suit in Suit:
            if suit not in non_wild_suits:
                missing_suits.append(suit)

        # Assign each wild card one of the missing suits.
        for i, wild in enumerate(wilds):
            self.wild_assignments[wild] = {
                'score': non_wilds[0].return_value(),
                'rank_index': non_wilds[0].return_rank_index(),
                'rank': non_wilds[0].rank,
                'suit': missing_suits[i]
            }

    def return_card_value(self, card, ruleset):
        """
        Return the score value of a card within this meld.

        Wild cards use their assigned replacement value.
        Aces may be scored as high or low depending on meld type and rules.

        Args:
            card: The card whose value is being calculated.
            ruleset: The active ruleset controlling scoring.

        Returns:
            int: The score value of the card in this meld.
        """
        if ruleset.is_wild(card):
            return self.wild_assignments[card]['score']

        if card.rank == "Ace":
            if self.meld_type == "set":
                if ruleset.ace_both or ruleset.ace_high:
                    return ruleset.ace_high_score
                else:
                    return 1

            if self.meld_type == "run":
                if self._is_ace_high_in_run(card, ruleset):
                    return ruleset.ace_high_score
                else:
                    return 1

        return card.return_value()

    def _is_ace_high_in_run(self, ace_card, ruleset):
        """
        Determine whether an Ace should be treated as high in a run.

        An Ace is treated as high if the run contains a King, either as a
        normal card or through a wild card assignment.

        Args:
            ace_card: The Ace card being checked.
            ruleset: The active ruleset used to identify wild cards.

        Returns:
            bool: True if the Ace should be scored high, otherwise False.
        """
        other_cards = [
            card for card in self.cards
            if card.rank != "Ace" and not ruleset.is_wild(card)
        ]

        has_king = any(card.rank == "King" for card in other_cards)

        for wild in self.wild_assignments:
            if self.wild_assignments[wild]['rank'] == "King":
                has_king = True
                break

        return has_king

    def return_meld_value(self, ruleset):
        """
        Calculate the total score of the meld.

        Args:
            ruleset: The active ruleset controlling scoring.

        Returns:
            int: The total value of all cards in the meld.
        """
        score = 0

        for card in self.cards:
            score += self.return_card_value(card, ruleset)

        return score

    def add_card(self, card):
        """
        Add a card to the meld.

        Args:
            card: The card to add.
        """
        self.cards.append(card)

    def wild_card_comparison(self, card, wild, ruleset):
        """
        Check whether a card can replace a wild card in the meld.

        Replacement is only allowed if the ruleset permits it, and if the
        card matches the rank and suit currently assigned to the wild card.

        Args:
            card: The card being compared.
            wild: The wild card currently in the meld.
            ruleset: The active ruleset controlling replacement behaviour.

        Returns:
            bool: True if the card can replace the wild card, otherwise False.
        """
        if ruleset.allow_wild_replacement:
            wild_assignment = self.wild_assignments[wild]
            return (
                card.rank == wild_assignment['rank']
                and card.suit == wild_assignment['suit']
            )
        else:
            return False

    def replace_wild(self, card, wild):
        """
        Replace a wild card in the meld with a normal card.

        The wild card is removed from the meld, the new card is added,
        and the stored wild assignment is deleted.

        Args:
            card: The card replacing the wild card.
            wild: The wild card being removed.

        Returns:
            The removed wild card.
        """
        self.cards.remove(wild)
        self.cards.append(card)

        if wild in self.wild_assignments:
            del self.wild_assignments[wild]

        return wild