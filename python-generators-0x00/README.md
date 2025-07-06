# Generator-Based Data Handling Tasks
This project demonstrates efficient ways to **retrieve**, **process**, and **aggregate data** from a MySQL database using Python **generators** to ensure **low-memory usage**, even when handling large datasets.

---

# Tasks Overview
## 1. Stream Rows from SQL Database (Row-by-Row)
- Implements a generator that connects to the `ALX_prodev` MySQL database and streams rows from the `user_data` table **one at a time**.
- Useful for handling large tables without loading everything into memory.
- **Function**: `stream_user_data(connection)`

---

## 2. Batch Processing with Filtering
- Streams users from the database in `batches` using `fetchmany()` and filters users whose **age is greater than 25**.
- Makes use of no more than three loops and utilizes generators to ensure performance.
- **Functions**:
  - `stream_users_in_batches(batch_size)`
  - `batch_processing(batch_size)`
  
---

## 3. Lazy Pagination
- Simulates **lazy-loading** of paginated results using `LIMIT` and `OFFSET` in SQL.
- Fetches the **next page only when needed**, reducing resource usage.
- Uses a generator to yield individual rows across pages.
- **Functions**:
  - `paginate_users(page_size, offset)`
  - `lazy_paginate(page_size)`

---

## 4. Memory-Efficient Average Calculation
- Computes the **average age** of users using a generator that yields one age ata a time.
- Avoids loading the entire table or using SQL aggregation (`AVG`).
- Ensures memory efficiency for large datasets using only **two loops**.
- **Functions**:
  - `stream_user_ages()`
  - `compute_average_age()`
  
---

## Technologies used
- Python 3
- MySQL
- `mysql-connector-python` for DB connectivity
- `csv` and `decimal` libraries for data handling and precision

---