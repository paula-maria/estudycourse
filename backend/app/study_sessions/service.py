from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.study_sessions.model import StudySession
from app.study_sessions.repository import StudySessionRepository


class StudySessionService:

    def __init__(self):
        self.repository = StudySessionRepository()

    def create(
        self,
        db: Session,
        data
    ):
        if data.duration_minutes <= 0:
            raise HTTPException(
                status_code=400,
                detail="Duration must be greater than zero"
            )

        session = StudySession(
            study_plan_subject_id=data.study_plan_subject_id,
            session_date=data.session_date,
            duration_minutes=data.duration_minutes,
            status="pending",
            created_at=datetime.utcnow()
        )

        return self.repository.create(
            db,
            session
        )

    def get(
        self,
        db: Session,
        session_id: int
    ):
        session = self.repository.get_by_id(
            db,
            session_id
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Study session not found"
            )

        return session

    def list_by_plan_subject(
        self,
        db: Session,
        study_plan_subject_id: int
    ):
        return self.repository.get_by_plan_subject(
            db,
            study_plan_subject_id
        )

    def update(
        self,
        db: Session,
        session_id: int,
        data
    ):
        session = self.get(
            db,
            session_id
        )

        values = data.model_dump(
            exclude_unset=True
        )

        if (
            "duration_minutes" in values
            and values["duration_minutes"] <= 0
        ):
            raise HTTPException(
                status_code=400,
                detail="Duration must be greater than zero"
            )

        for field, value in values.items():
            setattr(
                session,
                field,
                value
            )

        return self.repository.update(
            db,
            session
        )

    def complete(
        self,
        db: Session,
        session_id: int
    ):
        session = self.get(
            db,
            session_id
        )

        session.status = "completed"

        return self.repository.update(
            db,
            session
        )

    def delete(
        self,
        db: Session,
        session_id: int
    ):
        session = self.get(
            db,
            session_id
        )

        self.repository.delete(
            db,
            session
        )