import sqlite3


class ExecuteQuery:
    """
    Reusable context manager that takes a query as input
     and executes it, managing both connection
      and the query execution
    """

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(self.query, self.params)
            return list(self.cursor.fetchall())
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    database = "users.db"
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(database, query, params) as result:
        if result:
            for row in result:
                print(row)
        else:
            print("Query failed")
