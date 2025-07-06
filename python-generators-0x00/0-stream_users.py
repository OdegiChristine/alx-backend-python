import seed
from itertools import islice

# Uses a generator to fetch rows one by one
def stream_users():
    db_conn = seed.connect_to_prodev()
    cursor = db_conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_data')
    for row in cursor:
        yield row
    cursor.close()
    db_conn.close()

for user in islice(stream_users(), 10):
    print(user)
