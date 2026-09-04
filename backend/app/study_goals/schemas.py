from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.study_goals.enums import GoalStatus, GoalType


class StudyGoalCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    study_plan_id: int | None = None

    goal_type: GoalType

    target_value: int = Field(
        gt=0,
    )

    start_date: date

    end_date: date | None = None

    is_primary: bool = False


class StudyGoalUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    study_plan_id: int | None = None

    target_value: int | None = Field(
        default=None,
        gt=0,
    )

    start_date: date | None = None

    end_date: date | None = None

    status: GoalStatus | None = None

    is_primary: bool | None = None


class StudyGoalResponse(BaseModel):
    id: int
    user_id: int
    study_plan_id: int | None

    title: str
    description: str | None

    goal_type: GoalType

    target_value: int
    current_value: int

    start_date: date
    end_date: date | None

    status: GoalStatus
    is_primary: bool

    created_at: datetime
    updated_at: datetime

    progress_percentage: float

    model_config = ConfigDict(
        from_attributes=True
    )
