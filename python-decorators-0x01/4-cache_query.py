import time
import sqlite3
import functools

query_cache = {}

# Caches query results based on the SQL query string. Caches results to avoid redundant calls
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if query in query_cache:
            print("[CACHE] Returning cached results for query.")
            return query_cache[query]
        else:
            result = func(*args, **kwargs)
            query_cache[query] = result
            print("[CACHE] Caching results for query.")
            return result
    return wrapper


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        kwargs.setdefault('conn', conn)

        try:
            return func(*args, **kwargs)
        finally:
            conn.close()
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
