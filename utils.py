import mysql.connector

def execute_query(conn, query, params=None):
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    return result

def create_index(conn, table, column):
    query = f"CREATE INDEX idx_{table}_{column} ON {table} ({column})"
    execute_query(conn, query)

def drop_index(conn, table, column):
    query = f"DROP INDEX idx_{table}_{column} ON {table}"
    execute_query(conn, query)
