from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.study_goals.enums import GoalStatus, GoalType


class StudyGoal(Base):
    __tablename__ = "study_goals"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    study_plan_id: Mapped[int | None] = mapped_column(
        ForeignKey("study_plans.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    goal_type: Mapped[GoalType] = mapped_column(
        String(20),
        nullable=False,
    )

    target_value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    current_value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[GoalStatus] = mapped_column(
        String(20),
        nullable=False,
        default=GoalStatus.ACTIVE,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
