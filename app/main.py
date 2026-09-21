from fastapi import FastAPI

from app.api.routes import auth
from app.api.routes import categories
from app.api.routes import subscriptions

app = FastAPI(title="FinTrack API")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(subscriptions.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}