from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StudyPlanSubject(Base):
    __tablename__ = "study_plan_subjects"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    study_plan_id: Mapped[int] = mapped_column(
        ForeignKey("study_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    weekly_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )