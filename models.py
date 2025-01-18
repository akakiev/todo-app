from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Створюємо модель задачі (Task)
class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Categories", back_populates="tasks")

# Створюємо модель категорії (Category)
class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    tasks = relationship("Tasks", back_populates="category", cascade="all, delete")