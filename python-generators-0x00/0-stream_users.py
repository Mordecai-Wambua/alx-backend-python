import mysql.connector

def stream_users():
    """
    A generator that streams rows from an SQL database one by one.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mordecai@254",
            database="alx_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f'Error streaming users: {err}')
        return

        