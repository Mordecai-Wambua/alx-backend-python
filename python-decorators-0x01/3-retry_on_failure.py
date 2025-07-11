import time
import sqlite3 
import functools

def with_db_connection(func):
    """
    Automatically handles opening and closing database connections.
    """ 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        result = func(conn, *args, **kwargs)
        conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Retries database operations if they fail due to transient errors
    """ 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except sqlite3.Error as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts} failed: {e}")
                    if attempts >= retries:
                        print("[RETRY] All attempts failed.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)