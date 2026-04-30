from game_logic.card import Card
from game_logic.deck import Deck
from game_logic.ruleset import Ruleset
from game_logic.discard_pile import DiscardPile
from game_logic.validator import Validator
from game_logic.utils import Moves, quicksort
from game_logic.player import Player

from enum import Enum


class GameStatus(Enum):
    """Represents the current stage of the game."""

    LOBBY = "Lobby"
    IN_PROGRESS = "In Progress"
    GAME_OVER = "Game Over"
    PAUSED = "Paused"


class GameState:
    """
    Stores and manages the full state of a Rummy game.

    This class is responsible for:
    - tracking players
    - storing the deck and discard pile
    - managing turn order
    - applying player moves
    - checking win conditions
    - controlling game flow from lobby to game over
    """

    def __init__(self, player, ruleset=None, seed=None):
        """
        Create a new game state.

        Args:
            player: The player who creates the lobby.
            ruleset (Ruleset, optional): The ruleset to use for the game.
                If none is provided, a default Ruleset is created.
            seed (optional): Seed used for deterministic deck shuffling.
        """
        self.ruleset = ruleset or Ruleset()
        self.game_state = GameStatus.LOBBY

        # List of player objects currently in the game.
        # Initially, this only contains the player who created the lobby.
        self.players = [player]

        # Core game components. These are created when the game starts.
        self.deck: Deck
        self.discard_pile: DiscardPile
        self.table_melds = []
        self.winner = None

        # Stores the score a player must reach for their initial meld.
        self.current_required_meld_score = self.ruleset.min_initial_meld_score

        # Optional random seed for reproducible shuffling.
        self.seed = seed or None

        # Tracks whose turn it currently is.
        self.current_player_index = 0

    def update_ruleset(self, new_ruleset):
        """
        Update the ruleset before the game starts.

        Args:
            new_ruleset (Ruleset): The new ruleset to apply.

        Returns:
            tuple[bool, str]: Success status and message.
        """
        if self.game_state != GameStatus.LOBBY:
            return False, "Can't Change Rules After Game Began"

        self.ruleset = new_ruleset
        return True, "Rules Updated"

    def add_player(self, new_player):
        """
        Add a new player to the game lobby.

        Players can only be added while the game is still in the lobby.

        Args:
            new_player: The player object to add.

        Returns:
            str | None: Error message if the player cannot be added.
        """
        if self.game_state == GameStatus.LOBBY:
            if len(self.players) < self.ruleset.max_players:
                self.players.append(new_player)
            else:
                return "Game Has Begun"

    def ready(self, player):
        """
        Mark a player as ready.

        Args:
            player: The player to mark as ready.
        """
        player.ready = True

    def start_game(self, ruleset):
        """
        Start the game once all players are ready.

        This method:
        - checks that the game has not already started
        - checks that all players are ready
        - loads the chosen ruleset
        - creates and shuffles the deck
        - deals cards to all players
        - places the first card in the discard pile

        Args:
            ruleset (dict): Ruleset data to convert into a Ruleset object.

        Returns:
            tuple[bool, str]: Success status and message.
        """
        if self.game_state != GameStatus.LOBBY:
            return False, "Game Already Started"

        for player in self.players:
            if not player.ready:
                return False, "Not All Players Ready"

        # Convert dictionary data into a Ruleset object.
        new_ruleset = Ruleset.from_dict(ruleset)
        self.update_ruleset(new_ruleset)

        self.game_state = GameStatus.IN_PROGRESS

        # Create and shuffle the deck.
        self.deck = Deck(self.ruleset, self.seed)
        self.deck.shuffle()

        # Create an empty discard pile.
        self.discard_pile = DiscardPile()

        # Deal the starting hand to each player.
        for player in self.players:
            for _ in range(self.ruleset.initial_hand_size):
                player.hand.add_card(self.deck.draw())

        # Place the first card from the deck into the discard pile.
        self.discard_pile.push(self.deck.draw())

        return True, "Game Started"

    def pause_game(self):
        """Pause the game."""
        self.game_state = GameStatus.PAUSED

    def return_current_player(self):
        """
        Return the player whose turn it currently is.

        Returns:
            player: The current player object.
        """
        return self.players[self.current_player_index]

    def next_turn(self):
        """
        Advance to the next player's turn.

        Uses modulus so that turn order wraps back to the first player
        after the final player has taken their turn.
        """
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def draw_from_deck(self, player):
        """
        Allow a player to draw a card from the deck.

        Args:
            player: The player attempting to draw.

        Returns:
            tuple[bool, str | None]: Success status and optional error message.
        """
        if self.deck.empty_check():
            self._remake_deck()
        
        valid, error = Validator.validate_draw(
            self.deck,
            player.has_drawn
        )

        if valid:
            player.add_card(self.deck.draw())
            player.has_drawn = True
            return True, None
        else:
            return valid, error

    def draw_from_discard_pile(self, player):
        """
        Allow a player to draw the top card from the discard pile.

        Args:
            player: The player attempting to draw.

        Returns:
            tuple[bool, str | None]: Success status and optional error message.
        """
        valid, error = Validator.validate_draw_discard(
            self.discard_pile.peek(),
            self.discard_pile,
            player.has_drawn,
            player.has_melded,
            player.ruleset
        )

        if valid:
            card = self.discard_pile.draw_top_card()
            player.add_card(card)
            player.has_drawn = True
            player.drawn_from_discard_pile = card
            return valid, None
        else:
            return valid, error

    def play_stored_melds(self, player):
        """
        Play all melds currently stored by a player onto the table.

        This method validates the stored melds first. If valid, the cards
        are removed from the player's hand, added to the table melds, and
        the player's required meld score is updated if needed.

        Args:
            player: The player attempting to play melds.

        Returns:
            tuple[bool, str | list]: Success status and either an error
            message or validation result.
        """
        success, error_or_stored_melds = Validator.validate_play_melds(
            player.current_stored_melds,
            player.has_melded,
            self.ruleset,
            self.current_required_meld_score
        )

        if not success:
            return success, error_or_stored_melds

        # Remove melded cards from the player's hand.
        for meld in player.stored_melds:
            for card in meld.cards:
                player.hand.remove_card(card)

        # Add the validated melds to the shared table area.
        self.table_melds += player.current_stored_melds

        # Update the required meld score for future turns if needed.
        self.update_required_meld_score(
            player.return_stored_meld_score(self.ruleset)
        )

        # Move current stored melds into completed meld history.
        player.completed_stored_melds += player.current_stored_melds

        # Clear the player's temporary meld storage.
        player.reset_current_stored_melds()

        return success, error_or_stored_melds

    def discard(self, player, card):
        """
        Discard a card from the player's hand to the discard pile.

        If the discard is valid, the card is removed from the player's hand,
        added to the discard pile, and the turn passes to the next player.

        Args:
            player: The player discarding the card.
            card (Card): The card to discard.

        Returns:
            tuple[bool, str | None]: Success status and optional error message.
        """
        valid, error = Validator.validate_discard(
            card,
            player.hand.cards,
            player.has_drawn,
            player.drawn_from_discard,
            self.ruleset
        )

        if valid:
            player.hand.remove_card(card)
            self.discard_pile.push(card)
            self.next_turn()
            return True, None
        else:
            return False, error

    def lay_off(self, player, card, meld):
        """
        Add a card from a player's hand onto an existing meld on the table.

        Args:
            player: The player laying off the card.
            card (Card): The card to add.
            meld: The table meld to add the card to.

        Returns:
            tuple[bool, str | None]: Success status and optional error message.
        """
        valid, error = Validator.validate_lay_off(card, meld, self.ruleset)

        if valid:
            player.hand.remove_card(card)
            meld.add_card(card)
            return True, None
        else:
            return False, error

    def update_required_meld_score(self, score):
        """
        Update the current required initial meld score.

        Only increases the score if the ruleset allows incremental meld scores.

        Args:
            score (int): The score to compare against the current requirement.
        """
        if self.ruleset.initial_meld_increment:
            if self.current_required_meld_score < score:
                self.current_required_meld_score = score

    def game_end(self, winning_player):
        """
        Calculate end-of-game scores and placements.

        All non-winning players lose points based on their deadwood score.
        The winning player gains the winner bonus defined by the ruleset.
        Players are then sorted into placements.

        Args:
            winning_player: The player who won the game.
        """
        deadwoods = []

        for player in self.players:
            if player != winning_player:
                deadwood = player.hand.calculate_deadwood(self.ruleset)
                player.add_to_score(self.ruleset, -deadwood)
                deadwoods.append((player, deadwood))

        winning_player.add_to_score(self.ruleset, self.ruleset.winner_deadwood)
        deadwoods.append((winning_player, self.ruleset.winner_deadwood))

        # Sort players differently depending on the scoring system.
        if self.ruleset.scoring_method == 'negative':
            deadwoods = quicksort(deadwoods, key=lambda x: x[1])
        else:
            deadwoods = quicksort(deadwoods, key=lambda x: x[1], reverse=True)

        placement_results = {}

        # Assign placement numbers starting from 1st place.
        for place, (player, score) in enumerate(deadwoods):
            placement_results[place + 1] = (player, score)

        return placement_results

    def check_win_condition(self, player):
        """
        Check whether a player has won the game.

        A player wins when their hand is empty.

        Args:
            player: The player to check.

        Returns:
            player | None: The winning player if they have won, otherwise None.
        """
        if player.hand.is_empty():
            self.game_state = GameStatus.GAME_OVER
            self.winner = player
            return self.winner
        else:
            return None

    def return_game_state(self):
        """
        Return the current game status.

        Returns:
            GameStatus: The current state of the game.
        """
        return self.game_state

    def return_winner(self):
        """
        Return the winning player.

        Returns:
            player | None: The winner if the game is over, otherwise None.
        """
        return self.winner

    def get_player_by_id(self, user_id):
        """
        Find a player in the game using their ID.

        Args:
            user_id: The ID of the player to find.

        Returns:
            player | None: The matching player, or None if not found.
        """
        for player in self.players:
            if player.user_id == user_id:
                return player
        return None

    def _select_card(self, player, card):
        """
        Mark a card as selected for a player.

        Args:
            player: The player selecting the card.
            card (Card): The card to select.
        """
        player.select_card(card)

    def deselect_all(self, player):
        """
        Deselect all currently selected cards for a player.

        Args:
            player: The player whose cards should be deselected.
        """
        player.deselect_all()

    def _deselect_card(self, player, card):
        """
        Deselect a specific card for a player.

        Args:
            player: The player deselecting the card.
            card (Card): The card to deselect.
        """
        player.deselect_card(card)

    def _remake_deck(self):
        if not self.deck.empty_check():
            return True, None
        
        if self.discard_pile.is_empty() or len(self.discard_pile.cards) <= 1:
            return False, "Cannot remake deck due to insufficient cards in the discard pile."
        
        cards_to_remake = self.discard_pile.split_discard_pile()

        self.deck.add_cards(cards_to_remake)
        self.deck.shuffle()

        return True, None

    def _get_card_from_dict(self, card_dict):
        """
        Convert a dictionary representation of a card back into a Card object.

        Args:
            card_dict (dict): Dictionary form of a card.

        Returns:
            Card: The reconstructed card object.
        """
        return Card.from_dict(card_dict, self.ruleset)

    def apply_move(self, move):
        """
        Apply a move sent by a player.

        This acts as the main dispatcher for all move types. It reads the move
        data, identifies the player, and calls the relevant method.

        Args:
            move (dict): A dictionary containing move information, including:
                - move_type
                - user_id
                - any extra data needed for that move

        Returns:
            tuple[bool, str | None]: Success status and optional error message.
        """
        move_type = Moves[move["move_type"]]
        player = self.get_player_by_id(move.get("user_id"))
        if player is None:
            return False, "Player not found"

        if move_type == Moves.Draw_Deck:
            return self.draw_from_deck(player)

        elif move_type == Moves.Draw_Discard:
            return self.draw_from_discard_pile(player)

        elif move_type == Moves.Discard:
            card = self._get_card_from_dict(move["card"])
            valid, error = self.discard(player, card)
            if not valid:
                return False, error
            self.check_win_condition(player)
            return True, None

        elif move_type == Moves.Store_Meld:
            return player.store_meld(self.ruleset)

        elif move_type == Moves.Meld:
            return self.play_stored_melds(player)

        elif move_type == Moves.Lay_Off:
            card = self._get_card_from_dict(move["card"])
            meld = self.table_melds[move["meld_index"]]
            return self.lay_off(player, card, meld)

        elif move_type == Moves.Store_Card:
            card = self._get_card_from_dict(move["card"])
            self._select_card(player, card)
            return True, None

        elif move_type == Moves.Deselect_all:
            self.deselect_all(player)
            return True, None

        elif move_type == Moves.Sort_Rank:
            player.sort_rank()
            return True, None

        elif move_type == Moves.Sort_Suit:
            player.sort_suit()
            return True, None

        else:
            return False, "Unknown Move"