import sqlite3

# Reusable context manager that takes a query as input and executes it, managing both connection and the query execution
class ExecuteQuery:
    def __init__(self, query, par):
        self.query = query
        self.par = par
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.par)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as cursor:
    for row in cursor:
        print(row)
