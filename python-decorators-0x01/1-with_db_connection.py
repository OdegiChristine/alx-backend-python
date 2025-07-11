import sqlite3
import functools


# Opens a database connection, passes it to the function and closes it afterward
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db_conn = sqlite3.connect('users.db')
        kwargs.setdefault('conn', db_conn)

        try:
            return func(*args, **kwargs)
        finally:
            db_conn.close()
    return wrapper


### Fetch user by ID with automatic connection handling
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


user = get_user_by_id(user_id=1)
print(user)
