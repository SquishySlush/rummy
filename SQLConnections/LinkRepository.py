class LinkRepository:
    """
    Handles all database operations related to game history and friends.

    This repository is responsible for:
    - storing game history records
    - retrieving game history by player or game
    - updating and deleting game history
    - creating friend requests
    - updating friend request statuses
    - retrieving and deleting friends

    All methods return:
    (True, value) on success OR (False, error_message) on failure.
    """

    @staticmethod
    def create_game_history(db, user_id, game_id, result, role):
        """
        Store a game history record for a user.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.
            game_id (int): The ID of the game.
            result (str): The result of the game.
            role (str): The role the user had in the game.

        Returns:
            tuple: (True, None) after the record is stored.
        """
        db.execute(
            "INSERT INTO GameHistory(user_id, game_id, result, role) VALUES (%s, %s, %s, %s)",
            (user_id, game_id, result, role)
        )
        db.commit()

        return True, None

    @staticmethod
    def get_game_history_by_player(db, user_id):
        """
        Retrieve all game history records for a user.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, rows) if records are found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT * FROM GameHistory WHERE user_id = %s",
            (user_id,)
        )

        rows = result.fetchall()
        if not rows:
            return False, "No Game History Found"
        return True, rows

    @staticmethod
    def get_game_history_by_game(db, game_id):
        """
        Retrieve all game history records for a game.

        Args:
            db: The database connection object.
            game_id (int): The ID of the game.

        Returns:
            tuple: (True, rows) if records are found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT * FROM GameHistory WHERE game_id = %s",
            (game_id,)
        )

        rows = result.fetchall()
        if not rows:
            return False, "No Game History Found"
        return True, rows

    @staticmethod
    def delete_all_game_history_by_user(db, user_id):
        """
        Delete all game history records for a user.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, None) after deletion.
        """
        db.execute(
            "DELETE FROM GameHistory WHERE user_id = %s",
            (user_id,)
        )
        db.commit()

        return True, None

    @staticmethod
    def update_game_history(db, user_id, game_id, result):
        """
        Update a user's result for a specific game.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.
            game_id (int): The ID of the game.
            result (str): The updated game result.

        Returns:
            tuple: (True, None) after the record is updated.
        """
        db.execute(
            "UPDATE GameHistory SET result = %s WHERE user_id = %s AND game_id = %s",
            (result, user_id, game_id)
        )
        db.commit()

        return True, None

    @staticmethod
    def create_friends_list(db, user_id, friend_id):
        """
        Create a pending friend request.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user sending the request.
            friend_id (int): The ID of the user receiving the request.

        Returns:
            tuple: (True, None) after the request is stored.
        """
        db.execute(
            "INSERT INTO FriendsList(user_id, friend_id) VALUES (%s, %s)",
            (user_id, friend_id)
        )
        db.commit()

        return True, None

    @staticmethod
    def update_friend_status(db, sender_id, receiver_id, status):
        """
        Update the status of a pending friend request.

        If the request is accepted, a matching friend record is also created
        for the receiving user.

        Args:
            db: The database connection object.
            sender_id (int): The ID of the user who sent the request.
            receiver_id (int): The ID of the user responding to the request.
            status (str): The updated request status.

        Returns:
            tuple: (True, None) if updated, otherwise (False, error_message).
        """
        result = db.execute(
            """
            UPDATE FriendsList
            SET status = %s
            WHERE user_id = %s AND friend_id = %s AND status = 'Pending'
            """,
            (status, sender_id, receiver_id)
        )

        if result.rowcount == 0:
            return False, "Request Not Found Or Not Authorised"

        db.execute(
            """
            INSERT INTO FriendsList(user_id, friend_id, status)
            VALUES (%s, %s, %s)
            """,
            (receiver_id, sender_id, status)
        )

        db.commit()

        return True, None

    @staticmethod
    def get_friends(db, user_id):
        """
        Retrieve all accepted friends for a user.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, rows) if friends are found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT * FROM FriendsList WHERE user_id = %s AND status = %s",
            (user_id, "Accepted")
        )

        rows = result.fetchall()
        if not rows:
            return False, "No Friends Found"
        return True, rows

    @staticmethod
    def get_friends_by_status(db, user_id, status):
        """
        Retrieve friends or friend requests for a user by status.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.
            status (str): The friend request status to filter by.

        Returns:
            tuple: (True, rows) if records are found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT * FROM FriendsList WHERE user_id = %s AND status = %s",
            (user_id, status)
        )

        rows = result.fetchall()
        if not rows:
            return False, "No Requests Found"
        return True, rows

    @staticmethod
    def delete_friend(db, user_id, friend_id):
        """
        Delete a friend record between two users.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.
            friend_id (int): The ID of the friend.

        Returns:
            tuple: (True, None) after deletion.
        """
        db.execute(
            "DELETE FROM FriendsList WHERE user_id = %s AND friend_id = %s",
            (user_id, friend_id)
        )
        db.commit()

        return True, None

    @staticmethod
    def delete_friends_by_user(db, user_id):
        """
        Delete all friend records for a user.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, None) after deletion.
        """
        db.execute(
            "DELETE FROM FriendsList WHERE user_id = %s",
            (user_id,)
        )
        db.commit()

        return True, None