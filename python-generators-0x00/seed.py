import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

# Connect to the database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="######"  # Omitted for security purposes
    )

# Create database if it does not exist
def create_database(connection):
    # Create ALX_prodev databse if it doesn't exist
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created or already exists.")
    finally:
        cursor.close()

def connect_to_prodev():
    # Connect directly to ALX_prodev database
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="######",  # Omitted for security reasons
        database="ALX_prodev"
    )

def create_table(connection):
    # Create user_data table if it doesn't exist
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5, 2) NOT NULL,
        INDEX(user_id)
    )"""
    try:
        cursor.execute(query)
        print("table created or already exists.")
    finally:
        cursor.close()

def insert_data(connection, data):
    # Insert data into user_data table, skip if email already exists.
    cursor = connection.cursor()
    query = "SELECT email FROM user_data WHERE email = %s"
    insert_query = "INSERT INTO user_data (user_id, name, email, age) values (%s, %s, %s, %s)"

    inserted = 0
    for row in data:
        name, email, age = row
        cursor.execute(query, (email,))
        if not cursor.fetchone():
            uid = str(uuid.uuid4())
            cursor.execute(insert_query, (uid, name, email, float(age)))
            inserted += 1
    connection.commit()
    cursor.close()
    print(f"{inserted} rows inserted.")

def read_csv(filepath):
    # Read CSV and return rows excluding headers.
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # skip header
        return list(reader)

# Generator
def stream_user_data(connection):
    # Generator that yields user_data rows one by one
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()

if __name__ == '__main__':
    try:
        # Step 1: Connect and setup
        root_conn = connect_db()
        create_database(root_conn)
        root_conn.close()

        db_conn = connect_to_prodev()
        create_table(db_conn)

        # Step 2: Insert from csv
        csv_data = read_csv('python-generators-0x00/user_data.csv')
        insert_data(db_conn, csv_data)

        # Step 3: Stream rows using generator
        print("\nStreaming data from user_data table:")
        for row in stream_user_data(db_conn):
            print(row)

        db_conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
