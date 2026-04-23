from SQLConnections.DBConnections import DBConnection
from SQLConnections.UserRepository import UserRepository
from SQLConnections.GameRepository import GameRepository
from SQLConnections.MoveRepository import MoveRepository
from SQLConnections.LinkRepository import LinkRepository
from SQLConnections.Hashing import hash_password


class DatabaseService:
    """
    Acts as the service layer between the program and the repositories.

    This class combines repository methods where extra logic is needed,
    such as validating users, checking passwords, and formatting results.
    """

    def __init__(self):
        """
        Create the database service and open a database connection.
        """
        self.db = DBConnection()

    def close(self):
        """
        Close the database connection.
        """
        self.db.close()

    def sign_up(self, username, password, email):
        """
        Create a new user account.
        """
        return UserRepository.create_user(self.db, username, password, email)

    def log_in(self, username, password):
        """
        Log a user in by checking the entered password against the stored hash.
        """
        user, error = UserRepository.get_user_by_username(self.db, username)

        if user is None:
            return None, error

        stored_hash = user["password"]
        salt = user["salt"]

        _, hashed_password = hash_password(password, salt)

        if hashed_password == stored_hash:
            return user, None

        return None, "Incorrect Password"

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their ID.
        """
        return UserRepository.get_user_by_id(self.db, user_id)

    def change_password(self, user_id, old_password, new_password):
        """
        Change a user's password.
        """
        return UserRepository.change_password(self.db, user_id, old_password, new_password)

    def change_username(self, user_id, new_username):
        """
        Change a user's username.
        """
        return UserRepository.change_username(self.db, user_id, new_username)

    def delete_user(self, user_id):
        """
        Delete a user and all related records linked to that user.
        """
        MoveRepository.delete_all_moves_by_user(self.db, user_id)
        LinkRepository.delete_friends_by_user(self.db, user_id)
        LinkRepository.delete_all_game_history_by_user(self.db, user_id)

        return UserRepository.delete_user(self.db, user_id)

    def send_friend_request(self, user_id, friend_id):
        """
        Send a friend request from one user to another.
        """
        success, _ = UserRepository.get_user_by_id(self.db, user_id)
        if not success:
            return False, "Requesting User Not Found"

        success, _ = UserRepository.get_user_by_id(self.db, friend_id)
        if not success:
            return False, "Target User Not Found"

        return LinkRepository.create_friends_list(self.db, user_id, friend_id)

    def accept_friend_request(self, sender_id, receiver_id):
        """
        Accept a pending friend request.
        """
        return LinkRepository.update_friend_status(self.db, sender_id, receiver_id, "Accepted")

    def reject_friend_request(self, user_id, friend_id):
        """
        Reject or remove a pending friend request.
        """
        return LinkRepository.delete_friend(self.db, user_id, friend_id)

    def get_all_users_except(self, user_id):
        """
        Retrieve all users except the current user, excluding users who are
        already friends or already part of a pending request.
        """
        success, rows = UserRepository.get_all_users_except(self.db, user_id)
        if not success:
            return False, rows

        friend_ids = set()
        pending_ids = set()

        success, friends = self.get_friends(user_id)
        if success:
            for friend in friends:
                friend_ids.add(friend["user_id"])

        success, pending = self.get_pending_requests(user_id)
        if success:
            for request in pending:
                pending_ids.add(request["user_id"])

        other_users = []

        for user in rows:
            other_id = user["user_id"]

            if other_id in friend_ids or other_id in pending_ids:
                continue

            other_users.append({
                "user_id": other_id,
                "username": user["username"]
            })

        if other_users == []:
            return False, "No Users Found"

        return True, other_users

    def get_friends(self, user_id):
        """
        Retrieve all accepted friends for a user.
        """
        success, rows = LinkRepository.get_friends_by_status(self.db, user_id, "Accepted")
        if not success:
            return False, rows

        friends = []

        for row in rows:
            other_id = row["friend_id"]

            success, username = UserRepository.get_username_by_user_id(self.db, other_id)
            if success:
                friends.append({
                    "user_id": other_id,
                    "username": username
                })

        if friends == []:
            return False, "No Friends Found"

        return True, friends

    def get_pending_requests(self, user_id):
        """
        Retrieve all pending friend requests linked to a user.
        """
        success, rows = LinkRepository.get_pending_requests_for_user(self.db, user_id)
        if not success:
            return False, rows

        requests = []

        for row in rows:
            if row["user_id"] == user_id:
                other_id = row["friend_id"]
                direction = "outgoing"
            else:
                other_id = row["user_id"]
                direction = "incoming"

            success, username = UserRepository.get_username_by_user_id(self.db, other_id)
            if success:
                requests.append({
                    "user_id": other_id,
                    "username": username,
                    "direction": direction
                })

        if requests == []:
            return False, "No Pending Requests"

        return True, requests

    def create_game(self, ruleset, seed):
        """
        Create a new game in the lobby state.
        """
        return GameRepository.create_game(self.db, ruleset, "In Lobby", seed)

    def start_game(self, game_id):
        """
        Mark a game as in progress.
        """
        return GameRepository.change_status(self.db, game_id, "In Progress")

    def get_game(self, game_id):
        """
        Retrieve a game by its ID.
        """
        return GameRepository.get_game(self.db, game_id)

    def get_ruleset(self, game_id):
        """
        Retrieve the stored ruleset for a game.
        """
        return GameRepository.get_ruleset(self.db, game_id)

    def get_seed(self, game_id):
        """
        Retrieve the seed used for a game.
        """
        return GameRepository.get_seed(self.db, game_id)

    def get_games_in_lobby(self):
        """
        Retrieve all games currently in the lobby.
        """
        return GameRepository.get_games_by_status(self.db, "In Lobby")

    def pause_game(self, game_id):
        """
        Mark a game as paused.
        """
        return GameRepository.change_status(self.db, game_id, "Paused")

    def unpause_game(self, game_id):
        """
        Mark a paused game as back in progress.
        """
        return GameRepository.change_status(self.db, game_id, "In Progress")

    def get_paused_games_by_user(self, user_id):
        """
        Retrieve all paused games linked to a user.
        """
        result = self.db.execute(
            """SELECT Games.game_id FROM Games
               JOIN GameHistory ON Games.game_id = GameHistory.game_id
               WHERE GameHistory.user_id = %s AND Games.status = 'Paused'""",
            (user_id,)
        )

        rows = result.fetchall()
        if rows == []:
            return False, "No Paused Games Found"

        return True, rows

    def get_lobbies(self):
        """
        Retrieve all games currently in the lobby.
        """
        return GameRepository.get_games_by_status(self.db, "In Lobby")

    def get_game_status(self, game_id):
        """
        Retrieve the current status of a game.
        """
        return GameRepository.get_status(self.db, game_id)

    def delete_game(self, game_id):
        """
        Delete a game and all moves linked to it.
        """
        MoveRepository.delete_all_moves_in_game(self.db, game_id)
        return GameRepository.delete_game(self.db, game_id)

    def add_player_to_game(self, user_id, game_id, role):
        """
        Add a user to a game's history records.
        """
        return LinkRepository.create_game_history(self.db, user_id, game_id, "In Progress", role)

    def record_game_result(self, user_id, game_id, result):
        """
        Store the final result for a user in a game.
        """
        return LinkRepository.update_game_history(self.db, user_id, game_id, result)

    def get_player_history(self, user_id):
        """
        Retrieve the game history for a user.
        """
        success, rows = LinkRepository.get_game_history_by_user(self.db, user_id)
        if not success:
            return False, rows

        history = []

        for row in rows:
            user, error = UserRepository.get_user_by_id(self.db, row["user_id"])
            if user is None:
                continue

            history.append({
                "game_id": row["game_id"],
                "username": user["username"],
                "result": row["result"],
                "role": row["role"]
            })

        if history == []:
            return False, "No Game History Found"

        return True, history

    def get_game_players(self, game_id):
        """
        Retrieve all users linked to a game.
        """
        return LinkRepository.get_game_history_by_game(self.db, game_id)

    def add_move(self, game_id, user_id, move_type, card=None, cards=None, meld_index=None):
        """
        Add a move to a game using the next available move number.
        """
        success, move_count = MoveRepository.get_move_count(self.db, game_id)
        if not success:
            return False, move_count

        move_number = move_count + 1

        return MoveRepository.add_move(
            self.db,
            game_id,
            user_id,
            move_number,
            move_type,
            card=card,
            cards=cards,
            meld_index=meld_index
        )

    def get_moves(self, game_id):
        """
        Retrieve all moves stored for a game.
        """
        return MoveRepository.get_moves_by_game(self.db, game_id)

    def get_move_count(self, game_id):
        """
        Retrieve the number of moves stored for a game.
        """
        return MoveRepository.get_move_count(self.db, game_id)

    def get_user_guest_status(self, user_id):
        """
        Retrieve whether a user is a guest account.
        """
        return UserRepository.get_user_guest_status(self.db, user_id)