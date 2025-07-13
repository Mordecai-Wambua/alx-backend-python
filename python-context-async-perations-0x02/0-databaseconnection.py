import sqlite3


class DatabaseConnection:
    """
    Context manager to handle opening and closing database connections automatically
    """

    def __init__(self, database):
        self.database = database

    def __enter__(self):
        self.connection = sqlite3.connect(self.database)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


with DatabaseConnection("users.db") as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    for row in result:
        print(row)
