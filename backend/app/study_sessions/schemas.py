from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class StudySessionCreate(BaseModel):
    study_plan_subject_id: int
    session_date: date
    duration_minutes: int


class StudySessionUpdate(BaseModel):
    session_date: date | None = None
    duration_minutes: int | None = None


class StudySessionResponse(BaseModel):
    id: int
    study_plan_subject_id: int
    session_date: date
    duration_minutes: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )