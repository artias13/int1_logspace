import pytest
import mysql.connector

@pytest.fixture(scope="session")
def db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="test_database"
    )
    yield conn
    conn.close()
