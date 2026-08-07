from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class StudyPlanCreate(BaseModel):
    title: str
    description: str | None = None
    start_date: date
    end_date: date


class StudyPlanUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class StudyPlanResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    start_date: date
    end_date: date
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )