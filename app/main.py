from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth
from app.api.routes import categories
from app.api.routes import subscriptions
from app.api.routes import expenses
from app.api.routes import budgets

app = FastAPI(title="FinTrack API")

# 1. Настройка разрешённых истоков (Origins)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 2. Подключение Middleware для обработки CORS и OPTIONS-запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Важно: разрешает методы POST, GET, OPTIONS, DELETE и т.д.
    allow_headers=["*"],  # Важно: разрешает заголовки, включая Authorization и Content-Type
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(subscriptions.router)
app.include_router(expenses.router)
app.include_router(budgets.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}