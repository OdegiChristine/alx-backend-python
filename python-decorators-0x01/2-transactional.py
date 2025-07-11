import sqlite3
import functools

# Manages database transactions by automatically committing or rolling back changes(in case the wrapped function raises an error)
def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        if conn is None:
            raise ValueError("Database connection 'conn' cannot be None.")

        try:
            result = func(*args, **kwargs)
            conn.commit(result)
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction rolled back due to: {e}")
            raise
    return wrapper



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


### Update user's email with automatic transaction handling
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")