import json


class GameRepository:
    """
    Handles all database operations related to games.

    All methods return:
    (True, value) on success OR (False, error_message) on failure.
    """

    @staticmethod
    def create_game(db, ruleset, status, seed):
        """
        Create a new game record.

        The ruleset object is converted into JSON before storage.
        """
        ruleset_string = json.dumps(ruleset.to_dict())

        db.execute(
            "INSERT INTO Games (ruleset, status, seed) VALUES (%s, %s, %s)",
            (ruleset_string, status, seed)
        )
        db.commit()

        game_id = db.cursor.lastrowid
        return True, game_id

    @staticmethod
    def change_status(db, game_id, status):
        """
        Update the status of a game.
        """
        db.execute(
            "UPDATE Games SET status = %s WHERE game_id = %s",
            (status, game_id)
        )
        db.commit()

        return True, None

    @staticmethod
    def get_status(db, game_id):
        """
        Retrieve the status of a game.
        """
        result = db.execute(
            "SELECT status FROM Games WHERE game_id = %s",
            (game_id,)
        )

        row = result.fetchone()
        if row is None:
            return False, "Game Not Found"

        return True, row["status"]

    @staticmethod
    def get_game(db, game_id):
        """
        Retrieve full game record.
        """
        result = db.execute(
            "SELECT * FROM Games WHERE game_id = %s",
            (game_id,)
        )

        row = result.fetchone()
        if row is None:
            return False, "Game Not Found"

        return True, row

    @staticmethod
    def get_ruleset(db, game_id):
        """
        Retrieve and decode the stored ruleset.
        """
        result = db.execute(
            "SELECT ruleset FROM Games WHERE game_id = %s",
            (game_id,)
        )

        row = result.fetchone()
        if row is None:
            return False, "Game Not Found"

        return True, json.loads(row["ruleset"])

    @staticmethod
    def delete_game(db, game_id):
        """
        Delete a game record.
        """
        db.execute(
            "DELETE FROM Games WHERE game_id = %s",
            (game_id,)
        )
        db.commit()

        return True, None

    @staticmethod
    def get_games_by_status(db, status):
        """
        Retrieve all game IDs with a given status.
        """
        result = db.execute(
            "SELECT game_id FROM Games WHERE status = %s",
            (status,)
        )

        rows = result.fetchall()
        if not rows:
            return False, "No Games With That Status Found"

        return True, rows

    @staticmethod
    def get_seed(db, game_id):
        """
        Retrieve the seed used for a game.
        """
        result = db.execute(
            "SELECT seed FROM Games WHERE game_id = %s",
            (game_id,)
        )

        row = result.fetchone()
        if row is None:
            return False, "Game Does Not Exist"

        return True, row["seed"]