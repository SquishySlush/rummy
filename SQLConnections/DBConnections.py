import mysql.connector


class DBConnection:
    """
    Handles the connection to the MySQL database.

    This class is responsible for:
    - establishing a connection
    - executing SQL queries
    - committing transactions
    - closing the connection safely
    """

    def __init__(self):
        """
        Initialise a connection to the database and create a cursor.

        The cursor uses dictionary=True so query results are returned
        as dictionaries instead of tuples.
        """
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='pass123',
            database='house_rummy'
        )

        self.cursor = self.connection.cursor(dictionary=True)

    def execute(self, query, params=None):
        """
        Execute a SQL query.

        Args:
            query (str): The SQL query to run.
            params (tuple, optional): Parameters to safely insert into the query.

        Returns:
            cursor: The cursor after execution (used to fetch results).
        """
        self.cursor.execute(query, params or ())
        return self.cursor

    def commit(self):
        """
        Commit the current transaction to the database.

        This must be called after INSERT, UPDATE, or DELETE queries
        to save changes permanently.
        """
        self.connection.commit()

    def close(self):
        """
        Close the database cursor and connection.

        Should be called when the database is no longer needed
        to free resources.
        """
        self.cursor.close()
        self.connection.close()