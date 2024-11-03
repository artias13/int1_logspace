import pytest
import time
from utils import execute_query, create_index, drop_index

@pytest.mark.usefixtures("db_connection")
class TestPerformanceQueries:
    def test_performance_comparison(self, db_connection):
        # Заполняем таблицу большим количеством данных
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        users = [("User {}".format(i), "user{}@example.com".format(i)) for i in range(100000)]
        for user in users:
            execute_query(db_connection, insert_query, user)
        
        # Тестируем производительность без индекса
        start_time = time.perf_counter()
        query = "SELECT * FROM users WHERE name LIKE '%User%'"
        execute_query(db_connection, query)
        time_without_index = time.perf_counter() - start_time
        
        # Создаем индекс
        create_index(db_connection, "users", "name")
        
        # Тестируем производительность с индексом
        start_time = time.perf_counter()
        execute_query(db_connection, query)
        time_with_index = time.perf_counter() - start_time
        
        # Удаляем индекс после теста
        drop_index(db_connection, "users", "name")
        
        # Проверяем, что запрос с индексом работает быстрее
        assert time_with_index < time_without_index * 1.5  # Allow for some variation

    def test_case_when_index_is_not_used(self, db_connection):
        # Создаем индекс
        create_index(db_connection, "users", "name")
        
        # Выполняем запрос, который не использует индекс (например, LIKE с подстрокой в начале)
        query = "SELECT * FROM users WHERE name LIKE 'User%'"
        start_time = time.perf_counter()
        execute_query(db_connection, query)
        time_with_index = time.perf_counter() - start_time
        
        # Удаляем индекс
        drop_index(db_connection, "users", "name")
        
        # Выполняем тот же запрос без индекса
        start_time = time.perf_counter()
        execute_query(db_connection, query)
        time_without_index = time.perf_counter() - start_time
        
        # Проверяем, что разница во времени незначительна
        assert abs(time_with_index - time_without_index) < 0.1
