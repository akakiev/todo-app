from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Посилання на базу даних
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo_app.db"

# Створюємо об'єкт для взаємодії з базою даних
# Параметр connect_args={"check_same_thread": False} необхідний для роботи з SQLite
# Якщо ви використовуєте іншу базу даних, видаліть цей параметр
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Створюємо об'єкт сесії для взаємодії з базою даних
# autocommit=False - вимикає автозбереження
# autoflush=False - вимикає автоочищення
# bind=engine - підключає сесію до об'єкту engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Створюємо базовий клас для моделей
# Він буде використовуватися для створення моделей
# Якщо ви використовуєте іншу базу даних, замініть declarative_base() на свій базовий клас
Base = declarative_base()

