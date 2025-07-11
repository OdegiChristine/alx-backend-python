import time
import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        kwargs.setdefault('conn', conn)

        try:
            return func(*args, **kwargs)
        finally:
            conn.close()

    return wrapper


"""Decorator Factory"""
# Retries the function a certain number of times if it raises an exception
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[RETRY] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
            print("[RETRY] All retry attempts failed.")
            raise last_exception

        return wrapper

    return decorator


# Attempt to fetch users with automatic retry on failure
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


users = fetch_users_with_retry()
print(users)
