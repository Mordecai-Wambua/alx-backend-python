"""
    Script to set up sqlite database
"""
import sqlite3

database = "users.db"
connection = sqlite3.connect(database)
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL
    );
    """
)

cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("admin", "admin@localhost", 21))
cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("user", "user@localhost", 24))
cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("bob", "bob@localhost", 45))
cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("mark", "mark@localhost", 29))
cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("kelly", "kelly@localhost", 67))
cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("ian", "ian@localhost", 41))
cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("me", "me@localhost", 23))
cursor.execute("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", ("tech", "tech@localhost", 72))

connection.commit()
connection.close()
