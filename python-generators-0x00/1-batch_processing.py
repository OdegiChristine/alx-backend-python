from decimal import Decimal
import seed

# Generator: Stream in batches
def stream_users_in_batches(batch_size):
    # Yields rows in batches
    db_conn = seed.connect_to_prodev()
    cursor = db_conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_data')

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows # Each yield is a batch of rows

    cursor.close()
    db_conn.close()

# Processor: Filter users > 25
def batch_processing(batch_size):
    # processes user batches, yields users older than 25
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if Decimal(user['age']) > 25:
                yield user

# Usage
if __name__ == '__main__':
    print("Users over age 25:")
    for user in batch_processing(batch_size=3):
        print(user)
