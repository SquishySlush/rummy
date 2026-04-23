import json


class MoveRepository:
    """
    Handles all database operations related to moves.

    This repository is responsible for:
    - storing moves made during a game
    - retrieving moves for a game or user
    - deleting stored moves
    - counting how many moves exist in a game

    All methods return:
    (True, value) on success OR (False, error_message) on failure.
    """

    @staticmethod
    def add_move(db, game_id, user_id, move_number, move_type, card=None, cards=None, meld_index=None):
        """
        Store a move in the database.

        A move may involve either:
        - a single card
        - multiple cards
        - no card data

        Card data is converted into JSON before being stored.

        Args:
            db: The database connection object.
            game_id (int): The ID of the game.
            user_id (int): The ID of the user making the move.
            move_number (int): The order number of the move in the game.
            move_type (str): The type of move performed.
            card: A single card object involved in the move.
            cards: A list of card objects involved in the move.
            meld_index (int, optional): The index of the meld affected by the move.

        Returns:
            tuple: (True, move_id) after the move is stored.
        """
        if cards is not None:
            card_string = json.dumps([c.to_dict() for c in cards])
        elif card is not None:
            card_string = json.dumps(card.to_dict())
        else:
            card_string = None

        db.execute(
            "INSERT INTO Moves (game_id, user_id, move_number, move_type, card, meld_index) VALUES (%s, %s, %s, %s, %s, %s)",
            (game_id, user_id, move_number, move_type, card_string, meld_index)
        )
        db.commit()

        move_id = db.cursor.lastrowid
        return True, move_id

    @staticmethod
    def get_moves_by_game(db, game_id):
        """
        Retrieve all moves made in a game.

        Results are ordered by move number so the game can be replayed
        in the correct sequence.

        Args:
            db: The database connection object.
            game_id (int): The ID of the game.

        Returns:
            tuple: (True, rows) if moves are found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT * FROM Moves WHERE game_id = %s ORDER BY move_number ASC",
            (game_id,)
        )

        rows = result.fetchall()
        if not rows:
            return False, "No Moves Found For This Game"
        return True, rows

    @staticmethod
    def delete_all_moves_in_game(db, game_id):
        """
        Delete all moves stored for a game.

        Args:
            db: The database connection object.
            game_id (int): The ID of the game.

        Returns:
            tuple: (True, None) after deletion.
        """
        db.execute(
            "DELETE FROM Moves WHERE game_id = %s",
            (game_id,)
        )
        db.commit()

        return True, None

    @staticmethod
    def get_moves_by_user(db, user_id):
        """
        Retrieve all moves made by a specific user.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, rows) if moves are found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT move_id FROM Moves WHERE user_id = %s",
            (user_id,)
        )

        rows = result.fetchall()
        if not rows:
            return False, "No Moves Found For This User"
        return True, rows

    @staticmethod
    def delete_all_moves_by_user(db, user_id):
        """
        Delete all moves made by a specific user.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, None) after deletion.
        """
        db.execute(
            "DELETE FROM Moves WHERE user_id = %s",
            (user_id,)
        )
        db.commit()

        return True, None

    @staticmethod
    def get_move_count(db, game_id):
        """
        Count how many moves are stored for a game.

        Args:
            db: The database connection object.
            game_id (int): The ID of the game.

        Returns:
            tuple: (True, count) on success.
        """
        result = db.execute(
            "SELECT COUNT(*) AS count FROM Moves WHERE game_id = %s",
            (game_id,)
        )

        row = result.fetchone()
        return True, row["count"]