from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class StudentProfileCreate(BaseModel):
    study_goal: str
    exam_name: str
    exam_date: date
    weekly_hours: int
    study_days: str
    education_level: str
    experience_level: str
    preferred_shift: str


class StudentProfileUpdate(BaseModel):
    study_goal: str | None = None
    exam_name: str | None = None
    exam_date: date | None = None
    weekly_hours: int | None = None
    study_days: str | None = None
    education_level: str | None = None
    experience_level: str | None = None
    preferred_shift: str | None = None


class StudentProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    study_goal: str
    exam_name: str
    exam_date: date
    weekly_hours: int
    study_days: str
    education_level: str
    experience_level: str
    preferred_shift: str
    created_at: datetime
    updated_at: datetime
