import sqlite3
import functools

#### decorator to lof SQL queries

def log_queries(func):
    """
    Logs database queries executed by any function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        print(f'LOG: Executing the query: {query}')
        return func(*args, **kwargs)
    return wrapper
    

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)