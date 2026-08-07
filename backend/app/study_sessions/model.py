from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StudySession(Base):
    __tablename__ = "study_sessions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    study_plan_subject_id: Mapped[int] = mapped_column(
        ForeignKey(
            "study_plan_subjects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    session_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )