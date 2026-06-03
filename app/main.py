from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401 — imported so SQLModel registers the tables
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    yield
    # Shutdown code (if needed)

app = FastAPI(title="Sports Events API", description="A small REST API for managing sports events and their results.",lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Welcome to the Sports Events API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
