from fastapi import FastAPI
from app.api import books, categories
from app.db.db import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book API")

app.include_router(categories.router)
app.include_router(books.router)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
