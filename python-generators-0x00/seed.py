import mysql.connector
import csv
import uuid

def connect_db():
    """
    Connects to the mysql database server
    """
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = ''
        )
        return connection
    except mysql.connector.Error as e:
        print(f'Error connecting to database: {e}')
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except mysql.connector.Error as e:
        print(f'Error creating database: {e}')

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MYSQL
    """
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'ALX_prodev'
        )
        return connection
    except mysql.connector.Error as e:
        print(f'Error connecting to ALX_prodev: {e}')
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    """
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
            );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print(f'Error creating table: {e}')

def insert_data(connection, data):
    """
    Inserts data in the database if it does not exist
    """
    try:
        cursor = connection.cursor()
        with open(data, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = float(row['age'])

                cursor.execute('SELECT user_id FROM user_data WHERE email = %s', (email,))
                if cursor.fetchone():
                    continue

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
        connection.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print(f'Error inserting data: {e}')