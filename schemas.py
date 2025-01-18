from pydantic import BaseModel
from typing import List, Optional

# Створюємо модель базової задачі (TaskBase)
class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False

    class Config:
        schema_extra = {
            "example": {
                "title": "Вивчити FastAPI",
                "description": "Побудувати FastAPI app за допомогою Swagger UI.",
                "completed": False,
                "category_id": 1
            }
        }

class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    completed: bool = False
    category_id: int

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

# Створюємо модель задачі (Task)
class Task(TaskBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True

# Створюємо модель базової категорії (CategoryBase)
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

# Створюємо модель категорії (Category)
class Category(CategoryBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode = True