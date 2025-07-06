#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """
    Yields user ages one by one.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT age FROM user_data;')
    for row in cursor:
        yield row

    cursor.close()
    connection.close()

def average_age():
    """
    Calculates the average age.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age['age']
        count += 1

    average = total_age / count if count > 0 else 0
    print(f'Average age of users: {average:.2f}')


average_age()
