import json

class Ruleset:
    """
    Store and validate all configurable game rules for the rummy platform.

    A Ruleset object is created from an optional configuration dictionary.
    Each setting is validated before being stored, and defaults are used
    whenever a value is missing or invalid.

    Attributes:
        allow_sets (bool): Whether set melds are allowed.
        allow_runs (bool): Whether run melds are allowed.
        max_meld_size_run (int | None): Maximum size allowed for a run meld.
        min_initial_meld_score (int): Minimum score needed for the initial meld.
        initial_meld_increment (bool): Whether the initial meld requirement
            increases over time.
        wilds (list): A list of cards treated as wild cards.
        wild_deadwood_score (int): Deadwood score assigned to wild cards.
        scoring_method (str): The scoring system used in the game.
        ace_low (bool): Whether aces can be used as low cards.
        ace_high (bool): Whether aces can be used as high cards.
        ace_both (bool): Whether aces can be used as both high and low.
        ace_wrap_around (bool): Whether aces can wrap around in runs.
        ace_high_score (int): Score value used when an ace is high.
        initial_hand_size (int): Number of cards dealt to each player.
        min_meld_size (int): Minimum number of cards required in a meld.
        max_meld_size_set (int): Maximum size allowed for a set meld.
        num_decks (int): Number of decks used in the game.
        require_melding_to_draw_from_disc (bool): Whether a player must meld
            before drawing from the discard pile.
        require_melding_to_lay_off (bool): Whether a player must meld before
            laying off cards.
        allow_wild_replacement (bool): Whether wild cards can be replaced.
        allow_wild_only_melds (bool): Whether melds made entirely of wild cards
            are allowed.
        prevent_discard_same_card (bool): Whether the card just drawn can be
            discarded immediately.
        points_for_winning (int): Bonus points awarded for winning.
        max_deck_shuffle (int | None): Maximum number of times the deck can be
            reshuffled.
        winner_deadwood (int): Deadwood score awarded or counted for the winner.
        max_players (int): Maximum number of players allowed.
    """

    def __init__(self, config=None):
        """
        Initialise a Ruleset object from a configuration dictionary.

        Args:
            config (dict | None): A dictionary of rule values. If None,
                default values are used.
        """
        config = config or {}

        # Control which meld types are allowed. At least one should be enabled
        # or the game cannot be completed.
        self.allow_sets = self._get_validated(
            config,
            'allow_sets',
            True,
            bool
        )

        self.allow_runs = self._get_validated(
            config,
            'allow_runs',
            True,
            bool
        )

        # Define meld size restrictions and initial meld requirements.
        self.max_meld_size_run = self._get_validated(
            config,
            'max_meld_size_run',
            None,
            int,
            None,
            1,
            None
        )

        self.min_initial_meld_score = self._get_validated(
            config,
            'min_initial_meld_score',
            0,
            int,
            None,
            0,
            None
        )

        self.initial_meld_increment = self._get_validated(
            config,
            'initial_meld_increment',
            False,
            bool
        )

        # Store the cards that count as wild cards.
        self.wilds = self._get_validated(
            config,
            'wilds',
            [("Joker", 0)],
            list
        )

        self.wild_deadwood_score = self._get_validated(
            config,
            'wild_deadwood_score',
            25,
            int,
            None,
            0,
            None
        )

        # Choose the scoring method for the game.
        self.scoring_method = self._get_validated(
            config,
            'scoring_method',
            'negative',
            str,
            ['negative', 'positve']
        )

        # Control how aces behave in runs and scoring.
        self.ace_low = self._get_validated(
            config,
            'ace_low',
            False,
            bool
        )

        self.ace_high = self._get_validated(
            config,
            'ace_high',
            False,
            bool
        )

        self.ace_both = self._get_validated(
            config,
            'ace_both',
            True,
            bool
        )

        self.ace_wrap_around = self._get_validated(
            config,
            'wrap_around',
            False,
            bool
        )

        self.ace_high_score = self._get_validated(
            config,
            'ace_high_score',
            10,
            int,
            None,
            1
        )

        # Set core deck, hand, and meld sizing rules.
        self.initial_hand_size = self._get_validated(
            config,
            'initial_hand_size',
            14,
            int,
            None,
            1
        )

        self.min_meld_size = self._get_validated(
            config,
            'min_meld_size',
            3,
            int,
            None,
            1,
            self.initial_hand_size
        )

        self.max_meld_size_set = self._get_validated(
            config,
            'max_meld_size_set',
            4,
            int,
            None,
            1,
            self.initial_hand_size
        )

        self.num_decks = self._get_validated(
            config,
            'num_decks',
            2,
            int,
            None,
            1
        )

        # Control turn and meld interaction rules.
        self.require_melding_to_draw_from_disc = self._get_validated(
            config,
            'require_melding_to_draw_from_disc',
            True,
            bool
        )

        self.require_melding_to_lay_off = self._get_validated(
            config,
            'require_melding_to_lay_off',
            True,
            bool
        )

        self.allow_wild_replacement = self._get_validated(
            config,
            'allow_wild_replacement',
            True,
            bool
        )

        self.allow_wild_only_melds = self._get_validated(
            config,
            'allow_wild_only_melds',
            False,
            bool
        )

        self.prevent_discard_same_card = self._get_validated(
            config,
            'prevent_discard_same_card',
            True,
            bool
        )

        # Set scoring and game flow limits.
        self.points_for_winning = self._get_validated(
            config,
            'points_for_winning',
            25,
            int
        )

        self.max_deck_shuffle = self._get_validated(
            config,
            'max_deck_shuffle',
            None,
            int
        )

        self.winner_deadwood = self._get_validated(
            config,
            'winner_deadwood',
            25,
            int
        )

        self.max_players = self._get_validated(
            config,
            'max_players',
            4,
            int
        )

    def _get_validated(
        self,
        config,
        key,
        default,
        expected_type,
        allowed_values=None,
        min_value=None,
        max_value=None
    ):
        """
        Retrieve and validate a configuration value.

        If the value is missing, the default is used. If the value has the
        wrong type, is not in the allowed values list, or falls outside the
        allowed numeric range, the default is also used.

        Args:
            config (dict): The configuration dictionary.
            key (str): The key to retrieve.
            default: The fallback value if validation fails.
            expected_type: The required type for the value.
            allowed_values (list | None): Specific allowed values.
            min_value (int | None): Minimum allowed numeric value.
            max_value (int | None): Maximum allowed numeric value.

        Returns:
            The validated value, or the default if validation fails.
        """
        value = config.get(key, default)

        if value is not None and not isinstance(value, expected_type):
            return default

        if allowed_values is not None and value not in allowed_values:
            return default

        if min_value is not None and value is not None and value < min_value:
            return default

        if max_value is not None and value is not None and value > max_value:
            return default

        return value

    def is_wild(self, card):
        """
        Check whether a card is treated as a wild card.

        Args:
            card: The card to test.

        Returns:
            bool: True if the card's rank matches one of the configured
            wild cards, otherwise False.
        """
        return any(card.rank == t[0] for t in self.wilds)

    def to_dict(self):
        """
        Export the ruleset as a dictionary.

        This is useful for saving the ruleset or passing it between parts
        of the program.

        Returns:
            dict: A dictionary representation of the ruleset.
        """
        return {
            'allow_sets': self.allow_sets,
            'allow_runs': self.allow_runs,
            'min_meld_size': self.min_meld_size,
            'max_meld_size_set': self.max_meld_size_set,
            'max_meld_size_run': self.max_meld_size_run,
            'min_initial_meld_score': self.min_initial_meld_score,
            'initial_meld_increment': self.initial_meld_increment,
            'initial_hand_size': self.initial_hand_size,
            'num_decks': self.num_decks,
            'wilds': self.wilds,
            'scoring_method': self.scoring_method,
            'ace_high': self.ace_high,
            'ace_both': self.ace_both,
            'ace_high_score': self.ace_high_score
        }

    def to_json_file(self, filename):
        """
        Save the ruleset to a JSON file.

        Args:
            filename (str): The name of the file to write to.
        """
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def from_json_file(cls, filename):
        """
        Create a Ruleset object from a JSON file.

        Args:
            filename (str): The name of the JSON file to read.

        Returns:
            Ruleset: A new Ruleset object built from the file data.
        """
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls(data)

    @classmethod
    def from_dict(cls, dictionary):
        """
        Create a Ruleset object from a dictionary.

        Args:
            dictionary (dict): A dictionary containing ruleset values.

        Returns:
            Ruleset: A new Ruleset object built from the dictionary.
        """
        return cls(dictionary)