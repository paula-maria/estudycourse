from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.student_profiles.router import router as student_profiles_router
from app.users.router import router as users_router


app = FastAPI()


app.include_router(users_router)
app.include_router(student_profiles_router)


@app.get("/")
def root(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "message": "API is running",
        "database": "connected"
    }
