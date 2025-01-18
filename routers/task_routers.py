from fastapi import APIRouter, HTTPException, Depends
from models import Tasks, Categories
from typing import List
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import Task, TaskCreate, TaskUpdate

# Створюємо роутер для задач
# APIRouter - клас для створення роутерів
# tags - теги для документації
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ендпойнт для отримання усіх задач
@router.get("/tasks", response_model=List[Task], summary="Отримати усі задачі", description="Отримати список усіх завдань у базі даних.")
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Tasks).all()

# Ендпойнт для додавання задачі
@router.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    category = db.query(Categories).filter(Categories.id == task.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Не існує такого category_id")
    
    new_task = Tasks(**task.model_dump())  
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Ендпойнт для виправлення задачі
@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Tasks).filter(Tasks.id == task_id).first()  
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# Ендпойнт для видалення задачі
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Tasks).filter(Tasks.id == task_id).first()  
    if not db_task:
        raise HTTPException(status_code=404, detail="Завдання не знайдено")
    db.delete(db_task)
    db.commit()
    return {"detail": "Завдання видалено успішно"}