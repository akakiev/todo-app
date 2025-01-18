from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

# Створюємо клієнта для тестування
# Клієнт буде використовувати екземпляр класу FastAPI
# для виконання запитів та отримання відповідей
client = TestClient(app)

# Тестуємо ендпойнт для відображення головної сторінки
# Перевіряємо, чи відповідь має код 200
# Перевіряємо, чи відповідь містить очікуваний JSON об'єкт
# Перевіряємо, чи відповідь містить очікуваний текст
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Вітаємо Вас на вдосконаленому додатку з управління задачами!"}

# Тестуємо ендпойнт для відображення списку категорій
def test_read_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    # Перевіряємо, чи відповідь містить список
    assert isinstance(response.json(), list)


# Тестуємо ендпойнт для відображення списку задач
def test_read_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    # Перевіряємо, чи відповідь містить список
    assert isinstance(response.json(), list)

# Тестуємо ендпойнт для створення задачі
# Перед викликом ендпойнта створюємо категорію
# Перевіряємо, чи відповідь має код 200
# Перевіряємо, чи відповідь містить очікуваний JSON об'єкт
def test_create_task():
    client.post(
        "/categories",
        json={"name": "work"}
    )
    response = client.post(
        "/categories/work/tasks",
        json={"title": "Нова задача", "description": "Опис нової задачі", "completed": False}
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "Нова задача",
        "description": "Опис нової задачі",
        "completed": False
    }
    assert response.json()["title"] == "Нова задача"