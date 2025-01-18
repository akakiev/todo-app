from fastapi import FastAPI
from routers import category_routers, task_routers
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

# Створюємо таблиці в базі даних
Base.metadata.create_all(bind=engine)

# Створюємо екземпляр класу FastAPI
app = FastAPI(
    title="TODO App",
    description="Додаток для управління задачами",
    version="0.1.0",
)

# Додаємо CORS middleware для обробки запитів з інших доменів
# Дозволяємо запити з доменів, вказаних в списку origins
# Дозволяємо відправку кукісів та використання будь-яких методів та заголовків
origins = [
    "http://127.0.0.1:8080",  # Vue.js development server
    "http://localhost:8080",  # Alternate localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаємо роутери
app.include_router(category_routers.router)
app.include_router(task_routers.router)

# Ендпойнт для відображення головної сторінки
@app.get("/")
async def read_root():
    return {"message": "Вітаємо Вас на вдосконаленому додатку з управління задачами!"}

# Запускаємо сервер
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)