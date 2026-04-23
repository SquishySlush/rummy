from SQLConnections.Hashing import hash_password


class UserRepository:
    """
    Handles all database operations related to users.

    This repository is responsible for:
    - creating user accounts
    - retrieving user records
    - updating usernames and passwords
    - deleting users
    - checking login credentials
    - retrieving guest account status
    """

    @staticmethod
    def create_user(db, username, password, email, guest=False):
        """
        Create a new user account.

        The method first checks whether the username already exists.
        If not, the password is hashed and the new user is inserted
        into the Users table.

        Args:
            db: The database connection object.
            username (str): The username for the new account.
            password (str): The user's plain text password.
            email (str): The user's email address.
            guest (bool): Whether the account is a guest account.

        Returns:
            tuple: (True, user) if successful, otherwise (False, error_message).
        """
        if UserRepository._username_exists(db, username):
            return False, "Username Exists"

        salt, hashed_password = hash_password(password)

        db.execute(
            "INSERT INTO Users(username, password, email, salt, guest) VALUES (%s, %s, %s, %s, %s)",
            (username, hashed_password, email, salt, guest)
        )
        db.commit()

        user, _ = UserRepository.get_user_by_username(db, username)
        return True, user

    @staticmethod
    def _username_exists(db, username):
        """
        Check whether a username is already stored in the database.

        Args:
            db: The database connection object.
            username (str): The username to check.

        Returns:
            bool: True if the username exists, otherwise False.
        """
        result = db.execute(
            "SELECT 1 FROM Users WHERE username = %s",
            (username,)
        )

        return result.fetchone() is not None

    @staticmethod
    def get_user_by_username(db, username):
        """
        Retrieve a user record using a username.

        Args:
            db: The database connection object.
            username (str): The username to search for.

        Returns:
            tuple: (row, None) if found, otherwise (None, error_message).
        """
        result = db.execute(
            "SELECT * FROM Users WHERE username = %s",
            (username,)
        )

        row = result.fetchone()
        if row is None:
            return None, "User Not Found"
        return row, None

    @staticmethod
    def get_user_by_id(db, user_id):
        """
        Retrieve a user record using a user ID.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (row, None) if found, otherwise (None, error_message).
        """
        result = db.execute(
            "SELECT * FROM Users WHERE user_id = %s",
            (user_id,)
        )

        row = result.fetchone()
        if row is None:
            return None, "User Not Found"
        return row, None

    @staticmethod
    def change_password(db, user_id, password, new_password):
        """
        Change a user's password.

        The current password must be verified before the new password
        is hashed and stored.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.
            password (str): The user's current password.
            new_password (str): The new password to save.

        Returns:
            tuple: (True, None) if successful, otherwise (False, error_message).
        """
        result, error = UserRepository.verify_password(db, password, user_id)

        if result:
            salt, hashed_password = hash_password(new_password)
            db.execute(
                "UPDATE Users SET password = %s, salt = %s WHERE user_id = %s",
                (hashed_password, salt, user_id)
            )
            db.commit()
            return True, None

        return False, error

    @staticmethod
    def change_username(db, user_id, new_username):
        """
        Change a user's username.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.
            new_username (str): The new username to save.

        Returns:
            tuple: (True, None) after the update is completed.
        """
        db.execute(
            "UPDATE Users SET username = %s WHERE user_id = %s",
            (new_username, user_id)
        )
        db.commit()

        return True, None

    @staticmethod
    def delete_user(db, user_id):
        """
        Delete a user account from the database.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user to delete.

        Returns:
            tuple: (True, None) after the user is deleted.
        """
        db.execute(
            "DELETE FROM Users WHERE user_id = %s",
            (user_id,)
        )
        db.commit()

        return True, None

    @staticmethod
    def verify_password(db, password, user_id):
        """
        Check whether a supplied password matches the stored password.

        The stored salt is retrieved from the database and used to hash
        the entered password for comparison.

        Args:
            db: The database connection object.
            password (str): The password entered by the user.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, None) if the password is correct,
                   otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT password, salt FROM Users WHERE user_id = %s",
            (user_id,)
        )

        row = result.fetchone()
        if row is None:
            return False, "User Not Found"

        salt, hashed_password = hash_password(password, row["salt"])

        if hashed_password == row["password"]:
            return True, None

        return False, "Password Incorrect"

    @staticmethod
    def get_all_users_except(db, user_id):
        """
        Retrieve all users except the specified user.

        Results are returned in alphabetical order by username.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user to exclude.

        Returns:
            tuple: (True, rows) if users are found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT * FROM Users WHERE user_id != %s ORDER BY username ASC",
            (user_id,)
        )

        rows = result.fetchall()

        if rows == []:
            return False, "No Users Found"
        return True, rows

    @staticmethod
    def get_user_guest_status(db, user_id):
        """
        Retrieve whether a user account is marked as a guest account.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, row) if found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT guest FROM Users WHERE user_id = %s",
            (user_id,)
        )

        row = result.fetchone()

        if row is None:
            return False, "User Not Found"
        return True, row

    @staticmethod
    def get_username_by_user_id(db, user_id):
        """
        Retrieve a username using a user ID.

        Args:
            db: The database connection object.
            user_id (int): The ID of the user.

        Returns:
            tuple: (True, username) if found, otherwise (False, error_message).
        """
        result = db.execute(
            "SELECT username FROM Users WHERE user_id = %s",
            (user_id,)
        )

        row = result.fetchone()

        if row is None:
            return False, "User Not Found"
        return True, row["username"]