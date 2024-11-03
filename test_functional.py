import pytest
from utils import execute_query, create_index, drop_index

@pytest.mark.usefixtures("db_connection")
class TestFunctionalQueries:
    def test_like_queries_without_index(self, db_connection):
        # Заполняем таблицу данными
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        users = [("John Doe", "john@example.com"), ("Jane Smith", "jane@example.com")]
        for user in users:
            execute_query(db_connection, insert_query, user)
        
        # Выполняем запрос LIKE без индекса
        query = "SELECT * FROM users WHERE name LIKE '%Doe%'"
        result_without_index = execute_query(db_connection, query)
        
        # Проверяем результат
        assert len(result_without_index) == 1
        assert result_without_index[0][1] == "John Doe"

    def test_like_queries_with_index(self, db_connection):
        # Создаем индекс
        create_index(db_connection, "users", "name")

        # Выполняем запрос LIKE с индексом
        query = "SELECT * FROM users WHERE name LIKE '%Doe%'"
        result_with_index = execute_query(db_connection, query)
        
        # Проверяем результат
        assert len(result_with_index) == 1
        assert result_with_index[0][1] == "John Doe"

        # Удаляем индекс после теста
        drop_index(db_connection, "users", "name")
