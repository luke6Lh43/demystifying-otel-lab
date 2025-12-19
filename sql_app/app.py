import os
import time
import pymssql

SQL_USER = os.getenv("SQL_USER", "sa")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "YourStrong!Passw0rd")
SQL1_HOST = os.getenv("SQL1_HOST", "sql-server-1")
SQL2_HOST = os.getenv("SQL2_HOST", "sql-server-2")
SQL_PORT = int(os.getenv("SQL_PORT", 1433))
DB_NAME = os.getenv("DB_NAME", "TestDB")

def ensure_db_and_table(server):
    # Connect to master DB to create our DB if needed
    conn = pymssql.connect(server, SQL_USER, SQL_PASSWORD, database='master', port=SQL_PORT, login_timeout=10)
    cur = conn.cursor()
    cur.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{DB_NAME}') CREATE DATABASE {DB_NAME};")
    conn.commit()
    conn.close()
    # Connect to our DB, create table if needed
    conn = pymssql.connect(server, SQL_USER, SQL_PASSWORD, database=DB_NAME, port=SQL_PORT, login_timeout=10)
    cur = conn.cursor()
    cur.execute("""
        IF OBJECT_ID('dbo.TestTable', 'U') IS NULL
        CREATE TABLE dbo.TestTable (
            id INT IDENTITY PRIMARY KEY,
            info NVARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn

def write_data(conn, info):
    cur = conn.cursor()
    cur.execute("INSERT INTO dbo.TestTable (info) VALUES (%s);", (info,))
    conn.commit()

if __name__ == "__main__":
    while True:
        try:
            conn1 = ensure_db_and_table(SQL1_HOST)
            conn2 = ensure_db_and_table(SQL2_HOST)
            break
        except Exception as e:
            print("Waiting for SQL Servers...", e)
            time.sleep(5)
    i = 1
    while True:
        data = f"sample-{i}"
        write_data(conn1, data)
        write_data(conn2, data)
        print(f"Wrote '{data}' to both servers.")
        i += 1
        time.sleep(10)