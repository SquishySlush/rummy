import uuid
from game_logic.game_state import GameState, GameStatus
from game_logic.player import Player
from game_logic.hand import Hand


class GameService:
    """
    Handles the main game service logic for the application.

    This class manages:
    - active games currently running in memory
    - active players currently logged in
    - communication between the game logic and the database service
    - communication between the game logic and the frontend
    """

    def __init__(self, db_service):
        """
        Create a new GameService object.

        Args:
            db_service: The database service used to store and retrieve data.
        """
        self.active_games = {}
        self.active_players = {}
        self.db = db_service

    def create_game(self, user_id, ruleset, seed=None):
        """
        Create a new game for a player.

        The method first checks that the player is active and not already in
        another game. It then creates the game in the database and stores the
        game in memory.

        Args:
            user_id: The ID of the user creating the game.
            ruleset: The ruleset that will be used for the game.
            seed: Optional seed used for predictable deck generation.

        Returns:
            tuple: (game_id, None) if successful, otherwise (False, error_message).
        """
        success, player = self.get_active_player(user_id)
        if not success:
            return False, player

        in_game, game_id = self.get_player_current_game(user_id)
        if in_game:
            return False, "Player In Game"

        success, game_id = self.db.create_game(ruleset, seed)
        if not success:
            return False, "Could Not Create Game"

        game = GameState(player, ruleset, seed)
        self.active_games[game_id] = game
        return game_id, None

    def add_player(self, game_id, user_id):
        """
        Add an active player to a game lobby.

        A player can only be added if the game is still in the lobby state.

        Args:
            game_id: The ID of the game to join.
            user_id: The ID of the player joining the game.

        Returns:
            tuple: (True, game_id) if successful, otherwise (False, error_message).
        """
        success, player = self.get_active_player(user_id)
        if not success:
            return False, player

        game = self.active_games[game_id]
        if game.game_state != GameStatus.LOBBY:
            return False, "Game Not Available"

        game.add_player(player)
        return True, game_id

    def ready(self, user_id, game_id):
        """
        Mark a player as ready in a lobby.

        The player must exist in the lobby and the game must still be available.

        Args:
            user_id: The ID of the player marking themselves as ready.
            game_id: The ID of the game lobby.

        Returns:
            tuple: (True, game_id) if successful, otherwise (False, error_message).
        """
        success, player = self.get_active_player(user_id)
        if not success:
            return False, player

        success, players = self.get_lobby_players(game_id)
        for p in players:
            if p.user_id == user_id: # type: ignore
                game = self.active_games[game_id]
                if game.game_state != GameStatus.LOBBY:
                    return False, "Game Not Available"

                game.ready(player)
                return True, game_id

        return False, "Player Not in Lobby"

    def get_lobby_players(self, game_id):
        """
        Get a list of all players currently in a lobby.

        Args:
            game_id: The ID of the game lobby.

        Returns:
            tuple: (True, players_list) if successful, otherwise (False, error_message).
        """
        game = self.active_games.get(game_id)
        if game is None:
            return False, "Game Not Found"

        players = []
        for p in game.players:
            players.append(p)

        return True, players

    def start_game(self, game_id, ruleset):
        """
        Start a game from the lobby.

        This updates the game state, stores the game as started in the database,
        and records each player as part of the game.

        Args:
            game_id: The ID of the game to start.
            ruleset: The ruleset to apply.

        Returns:
            tuple: (True, None) if successful, otherwise (False, error_message).
        """
        game = self.active_games[game_id]
        success, error = game.start_game(ruleset)
        if not success:
            return False, error

        self.db.start_game(game.ruleset, game.deck.seed)

        for player in game.players:
            self.db.add_player_to_game(player.user_id, game_id, "Player")

        return True, None

    def pause_game(self, game_id):
        """
        Pause a currently active game.

        The game is saved through the database and then removed from active memory.

        Args:
            game_id: The ID of the game to pause.

        Returns:
            tuple: (True, None) if successful, otherwise (False, error_message).
        """
        game = self.active_games[game_id]
        if game is None:
            return False, "Game Not Found"

        self.db.pause_game(game_id)
        game.pause_game()
        del self.active_games[game_id]
        return True, None

    def load_paused_game(self, game_id, user_id):
        """
        Load a paused game back into active memory.

        The method checks that:
        - the user is active
        - the game exists and is paused
        - the user belongs to that game

        Args:
            game_id: The ID of the paused game.
            user_id: The ID of the player loading the game.

        Returns:
            tuple: (True, "Game Loaded") if successful, otherwise (False, error_message).
        """
        success, player = self.get_active_player(user_id)
        if not success:
            return False, player

        row, error = self.db.get_game_status(game_id)
        if row is None:
            return False, error

        if row["status"] != "Paused":
            return False, "Game is not paused"

        history, error = self.db.get_player_history(player.user_id) #type: ignore
        if not history:
            return False, error

        if not any(row["game_id"] == game_id for row in history):
            return False, "Player Does Not Belong to This Game"

        ruleset, _ = self.db.get_ruleset(game_id)
        seed, _ = self.db.get_seed(game_id)

        game = GameState(player, ruleset, seed)
        self.active_games[game_id] = game
        return True, "Game Loaded"

    def rejoin_game(self, game_id, user_id):
        """
        Allow a player to rejoin a game they previously belonged to.

        Args:
            game_id: The ID of the game to rejoin.
            user_id: The ID of the player rejoining.

        Returns:
            tuple: (True, None) if successful, otherwise (False, error_message).
        """
        success, player = self.get_active_player(user_id)
        if not success:
            return False, player

        history, error = self.db.get_player_history(player.user_id) #type: ignore
        if not history:
            return False, error

        game_ids = [row["game_id"] for row in history]
        if game_id not in game_ids:
            return False, "Player Doesn't Belong to This Game"

        self.add_player(game_id, user_id)
        return True, None

    def resume_game(self, game_id):
        """
        Resume a paused game by replaying saved moves.

        Args:
            game_id: The ID of the game to resume.

        Returns:
            tuple: (True, "Game Resumed") if successful, otherwise (False, error_message).
        """
        game = self.active_games[game_id]
        moves, error = self.db.get_moves(game_id)

        if not moves:
            return False, error

        # Reapply each saved move so the game returns to its previous state.
        for move in moves:
            game.apply_move(move)

        return True, "Game Resumed"

    def apply_move(self, game_id, move):
        """
        Apply a player's move to the game.

        If the move is valid, it is stored in the database. If the move causes
        the game to finish, the game is ended automatically.

        Args:
            game_id: The ID of the game being played.
            move: A dictionary containing move information.

        Returns:
            tuple: (success, error_message_or_None)
        """
        game = self.active_games[game_id]
        success, error = game.apply_move(move)

        if success:
            self.db.add_move(
                game_id,
                move["user_id"],
                move["move_type"],
                move.get("card"),
                move.get("cards"),
                move.get("meld_index")
            )

            # If the game is over after this move, save the final results.
            if game.return_game_state() == GameStatus.GAME_OVER:
                self.end_game(game_id)

        return success, error

    def end_game(self, game_id):
        """
        End a game and store the final results.

        Each player's final placing and score is recorded in the database before
        the game is removed from active memory.

        Args:
            game_id: The ID of the game to end.

        Returns:
            tuple: (True, results) if successful, otherwise (False, error_message).
        """
        game = self.active_games[game_id]
        if game is None:
            return False, "Game Not Found"

        results = game.game_end(game.winner)

        for place, (player, score) in results.items():
            self.db.record_game_result(player.user_id, game_id, place, score)

        del self.active_games[game_id]
        return True, results

    def get_game_state(self, game_id, user_id):
        """
        Build and return the full visible game state for a player.

        This includes information such as:
        - current turn
        - top discard card
        - deck size
        - player's hand
        - table melds
        - scores
        - winner if the game has ended

        Args:
            game_id: The ID of the game.
            user_id: The ID of the player requesting the game state.

        Returns:
            dict or tuple: Game state dictionary if successful, otherwise
            (False, error_message).
        """
        player, error = self.get_active_player(user_id)
        if player is None:
            return False, error

        game = self.active_games[game_id]

        game_status = game.game_state.value
        current_player = game.return_current_player().user_id
        discard_top = game.discard_pile.peek().to_dict()
        deck_size = len(game.deck.cards)
        has_drawn = player.has_drawn #type: ignore
        has_melded = player.has_melded #type: ignore
        required_meld_score = game.current_required_meld_score
        winner = game.winner.user_id if game.winner else None

        # Convert the player's hand into a list of dictionaries for easy use by the UI.
        hand = []
        for card in player.hand.cards: #type: ignore
            hand.append(card.to_dict())

        # Convert all melds on the table into nested lists of card dictionaries.
        table_melds = []
        for meld in game.table_melds:
            meld_cards = []
            for card in meld.cards:
                meld_cards.append(card.to_dict())
            table_melds.append(meld_cards)

        # Store summary information for each player in the game.
        players = []
        for p in game.players:
            players.append({
                "user_id": p.user_id,
                "username": p.username,
                "hand_size": len(p.hand.cards),
                "score": p.score
            })

        # Store the cards currently selected by the player.
        selected_cards = []
        for card in player.get_stored_cards(): #type: ignore
            selected_cards.append(card.to_dict())

        state = {
            "game_status": game_status,
            "current_player": current_player,
            "discard_top": discard_top,
            "deck_size": deck_size,
            "has_drawn": has_drawn,
            "has_melded": has_melded,
            "required_meld_score": required_meld_score,
            "hand": hand,
            "selected_cards": selected_cards,
            "table_melds": table_melds,
            "players": players,
            "winner": winner
        }

        return state

    def get_active_player(self, user_id):
        """
        Find an active player currently stored in memory.

        Args:
            user_id: The ID of the user to find.

        Returns:
            tuple: (True, player) if found, otherwise (False, error_message).
        """
        player = self.active_players.get(user_id)
        if player is None:
            return False, "Player Not Found"
        return True, player

    def create_guest(self):
        """
        Create a guest account and log that guest into active memory.

        A random guest username is generated automatically.

        Returns:
            tuple: (True, user_data) if successful, otherwise (False, error_message).
        """
        username = f"Guest_{uuid.uuid4().hex[:8]}"
        success, user = self.db.sign_up(username, None, None)
        if not success:
            return False, "Could Not Create Guest"

        hand = Hand()
        player = Player(user["user_id"], username, hand)
        self.active_players[user["user_id"]] = player
        return True, user

    def get_lobbies(self):
        """
        Get all available game lobbies from the database.

        Returns:
            The result returned by the database service.
        """
        return self.db.get_lobbies()

    def get_paused_game(self, user_id):
        """
        Get paused games associated with a user.

        Args:
            user_id: The ID of the user.

        Returns:
            The result returned by the database service.
        """
        return self.db.get_paused_games_by_user(user_id)

    def sign_up(self, username, password, email):
        """
        Create a new registered user account.

        Args:
            username: The user's chosen username.
            password: The user's chosen password.
            email: The user's email address.

        Returns:
            The result returned by the database service.
        """
        return self.db.sign_up(username, password, email)

    def log_in(self, username, password):
        """
        Log a user in and create their active Player object.

        Args:
            username: The user's username.
            password: The user's password.

        Returns:
            tuple: (True, user_data) if successful, otherwise (False, error_message).
        """
        user, error = self.db.log_in(username, password)
        if user:
            hand = Hand()
            player = Player(user["user_id"], username, hand)
            self.active_players[user["user_id"]] = player
            return True, user
        return False, error

    def log_out(self, user_id, is_guest):
        """
        Log a user out of the system.

        If the user is a guest, their account is deleted as part of logout.

        Args:
            user_id: The ID of the user logging out.
            is_guest: Boolean value showing whether the user is a guest.

        Returns:
            tuple: (True, "Logged Out") if successful, otherwise (False, error_message).
        """
        user, _ = self.db.get_user_by_id(user_id)

        if user is None:
            return False, "No User To Log Out"

        if is_guest:
            self.delete_account(user_id)

        if user_id in self.active_players:
            del self.active_players[user_id]

        return True, "Logged Out"

    def delete_account(self, user_id):
        """
        Delete a user account.

        Args:
            user_id: The ID of the user account to delete.

        Returns:
            The result returned by the database service.
        """
        return self.db.delete_user(user_id)

    def change_password(self, user_id, old_password, new_password):
        """
        Change a user's password.

        Args:
            user_id: The ID of the user.
            old_password: The user's current password.
            new_password: The new password to set.

        Returns:
            The result returned by the database service.
        """
        return self.db.change_password(user_id, old_password, new_password)

    def change_username(self, user_id, new_username):
        """
        Change a user's username.

        Args:
            user_id: The ID of the user.
            new_username: The new username.

        Returns:
            The result returned by the database service.
        """
        return self.db.change_username(user_id, new_username)

    def send_friend_request(self, user_id, friend_id):
        """
        Send a friend request from one user to another.

        Args:
            user_id: The sender's user ID.
            friend_id: The recipient's user ID.

        Returns:
            The result returned by the database service.
        """
        return self.db.send_friend_request(user_id, friend_id)

    def accept_friend_request(self, user_id, friend_id):
        """
        Accept a friend request.

        Args:
            user_id: The user accepting the request.
            friend_id: The user who sent the request.

        Returns:
            The result returned by the database service.
        """
        return self.db.accept_friend_request(user_id, friend_id)

    def reject_friend_request(self, user_id, friend_id):
        """
        Reject a friend request.

        Args:
            user_id: The user rejecting the request.
            friend_id: The user who sent the request.

        Returns:
            The result returned by the database service.
        """
        return self.db.reject_friend_request(user_id, friend_id)

    def get_friends(self, user_id):
        """
        Get a user's list of friends.

        Args:
            user_id: The ID of the user.

        Returns:
            The result returned by the database service.
        """
        return self.db.get_friends(user_id)

    def get_pending_requests(self, user_id):
        """
        Get all pending friend requests for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            The result returned by the database service.
        """
        return self.db.get_pending_requests(user_id)

    def get_all_users_except(self, user_id):
        """
        Get all users except the specified user.

        Args:
            user_id: The ID of the user to exclude.

        Returns:
            The result returned by the database service.
        """
        return self.db.get_all_users_except(user_id)

    def get_player_history(self, user_id):
        """
        Get the full game history of a player.

        Args:
            user_id: The ID of the user.

        Returns:
            The result returned by the database service.
        """
        return self.db.get_player_history(user_id)

    def get_player_current_game(self, user_id):
        """
        Check whether a player is already in an active game.

        Args:
            user_id: The ID of the player.

        Returns:
            tuple: (True, game_id) if found, otherwise (False, error_message).
        """
        for game_id, game in self.active_games.items():
            if any(p.user_id == user_id for p in game.players):
                return True, game_id
        return False, "Could Not Find Game"

    def get_user_guest_status(self, user_id):
        """
        Get whether a user account is a guest account.

        Args:
            user_id: The ID of the user.

        Returns:
            The result returned by the database service.
        """
        return self.db.get_user_guest_status(user_id)