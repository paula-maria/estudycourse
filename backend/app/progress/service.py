from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.progress.repository import ProgressRepository


class ProgressService:

    def __init__(self):
        self.repository = ProgressRepository()

    def get_user_progress(
        self,
        db: Session,
        user_id: int,
    ):
        sessions = self.repository.get_user_sessions(
            db,
            user_id,
        )

        total_sessions = len(sessions)

        completed_sessions = sum(
            1
            for session in sessions
            if session.status == "completed"
        )

        pending_sessions = sum(
            1
            for session in sessions
            if session.status == "pending"
        )

        total_minutes = sum(
            session.duration_minutes
            for session in sessions
            if session.status == "completed"
        )

        total_hours = round(
            total_minutes / 60,
            2,
        )

        progress_percentage = (
            round(
                completed_sessions
                / total_sessions
                * 100,
                2,
            )
            if total_sessions > 0
            else 0.0
        )

        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "pending_sessions": pending_sessions,
            "total_minutes": total_minutes,
            "total_hours": total_hours,
            "progress_percentage": progress_percentage,
        }

    def get_plan_progress(
        self,
        db: Session,
        study_plan_id: int,
        user_id: int,
    ):
        sessions = self.repository.get_plan_sessions(
            db,
            study_plan_id,
            user_id,
        )

        if not sessions:
            raise HTTPException(
                status_code=404,
                detail="Study plan not found or has no sessions",
            )

        total_sessions = len(sessions)

        completed_sessions = sum(
            1
            for session in sessions
            if session.status == "completed"
        )

        pending_sessions = sum(
            1
            for session in sessions
            if session.status == "pending"
        )

        total_minutes = sum(
            session.duration_minutes
            for session in sessions
            if session.status == "completed"
        )

        total_hours = round(
            total_minutes / 60,
            2,
        )

        progress_percentage = round(
            completed_sessions
            / total_sessions
            * 100,
            2,
        )

        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "pending_sessions": pending_sessions,
            "total_minutes": total_minutes,
            "total_hours": total_hours,
            "progress_percentage": progress_percentage,
        }

    def get_subjects_progress(
        self,
        db: Session,
        user_id: int,
    ):
        subjects = self.repository.get_subject_progress(
            db,
            user_id,
        )

        result = []

        for subject in subjects:
            total_sessions = subject.total_sessions or 0
            completed_sessions = subject.completed_sessions or 0
            total_minutes = subject.total_minutes or 0

            pending_sessions = (
                total_sessions - completed_sessions
            )

            total_hours = round(
                total_minutes / 60,
                2,
            )

            progress_percentage = (
                round(
                    completed_sessions
                    / total_sessions
                    * 100,
                    2,
                )
                if total_sessions > 0
                else 0.0
            )

            result.append(
                {
                    "subject_id": subject.id,
                    "subject_name": subject.subject_name,
                    "total_sessions": total_sessions,
                    "completed_sessions": completed_sessions,
                    "pending_sessions": pending_sessions,
                    "total_minutes": total_minutes,
                    "total_hours": total_hours,
                    "progress_percentage": progress_percentage,
                }
            )

        return result

    def get_daily_progress(
        self,
        db: Session,
        user_id: int,
    ):
        daily_records = self.repository.get_daily_progress(
            db,
            user_id,
        )

        result = []
        for record in daily_records:
            result.append(
                {
                    "date": str(record.date),
                    "minutes_studied": record.minutes_studied or 0,
                    "sessions_completed": record.sessions_completed or 0,
                }
            )

        return result

    def get_dashboard(
        self,
        db: Session,
        user_id: int,
    ):
        summary = self.get_user_progress(db, user_id)
        subjects = self.get_subjects_progress(db, user_id)
        daily_progress = self.get_daily_progress(db, user_id)

        return {
            "summary": summary,
            "subjects": subjects,
            "daily_progress": daily_progress,
        }