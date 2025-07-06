import seed
from decimal import Decimal

# Stream ages one by one
def stream_user_ages():
    """
    Yields user ages one by one from user_data table
    """
    conn = seed.connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute('SELECT age FROM user_data')

    for (age,) in cursor:
        yield age

    cursor.close()
    conn.close()

# Compute Average age
def compute_average_age():
    """
    Uses a generator to compute the average age of all users ages in a memory-efficient way.
    """
    total = Decimal(0)
    count = 0

    for age in stream_user_ages():
        total += Decimal(age)
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")

# Main
if __name__ == '__main__':
    compute_average_age()
