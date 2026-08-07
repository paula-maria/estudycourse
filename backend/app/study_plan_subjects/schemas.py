from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudyPlanSubjectCreate(BaseModel):
    subject_id: int
    weekly_hours: int


class StudyPlanSubjectUpdate(BaseModel):
    weekly_hours: int


class StudyPlanSubjectResponse(BaseModel):
    id: int
    study_plan_id: int
    subject_id: int
    weekly_hours: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )