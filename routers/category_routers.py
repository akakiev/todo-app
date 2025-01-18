from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Categories
from database import SessionLocal
from schemas import Category, CategoryCreate
from typing import List

# Створюємо роутер для категорій
# APIRouter - клас для створення роутерів
# tags - теги для документації
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Створюємо кілька категорій
# Ендпойнт для отримання всіх категорій
@router.get("/categories", response_model=List[Category])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Categories).all()

# Ендпойнт для додавання категорії
@router.post("/categories", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Categories).filter(Categories.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Категорія вже існує")
    new_category = Categories(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Ендпойнт для редагування категорії
@router.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Categories).filter(Categories.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Категорія не знайдена")
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

# Ендпойнт для видалення категорії
@router.delete("/categories/{category_id}")
def delete_categoty(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Categories).filter(Categories.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Категорія не знайдена")
    db.delete(db_category)
    db.commit()
    return {"detail": "Категорія успішно видалена"}
    


