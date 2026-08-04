from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

app = FastAPI()


@app.get("/")
def root(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "message": "API is running",
        "database": "connected"
    }