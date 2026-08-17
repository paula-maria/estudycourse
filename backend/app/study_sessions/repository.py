from sqlalchemy import func
from sqlalchemy.orm import Session

from app.study_sessions.model import StudySession
from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plans.model import StudyPlan


class StudySessionRepository:

    def create(
        self,
        db: Session,
        session: StudySession
    ):
        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    def get_plan_subject_for_user(
        self,
        db: Session,
        study_plan_subject_id: int,
        user_id: int
    ):
        return (
            db.query(StudyPlanSubject)
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id
            )
            .filter(
                StudyPlanSubject.id == study_plan_subject_id,
                StudyPlan.user_id == user_id
            )
            .first()
        )

    def get_by_id_for_user(
        self,
        db: Session,
        session_id: int,
        user_id: int
    ):
        return (
            db.query(StudySession)
            .join(
                StudyPlanSubject,
                StudyPlanSubject.id == StudySession.study_plan_subject_id
            )
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id
            )
            .filter(
                StudySession.id == session_id,
                StudyPlan.user_id == user_id
            )
            .first()
        )

    def get_by_plan_subject_for_user(
        self,
        db: Session,
        study_plan_subject_id: int,
        user_id: int
    ):
        return (
            db.query(StudySession)
            .join(
                StudyPlanSubject,
                StudyPlanSubject.id == StudySession.study_plan_subject_id
            )
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id
            )
            .filter(
                StudySession.study_plan_subject_id
                == study_plan_subject_id,
                StudyPlan.user_id == user_id
            )
            .order_by(
                StudySession.session_date
            )
            .all()
        )

    def update(
        self,
        db: Session,
        session: StudySession
    ):
        db.commit()
        db.refresh(session)

        return session

    def delete(
        self,
        db: Session,
        session: StudySession
    ):
        db.delete(session)
        db.commit()

    def get_progress(
        self,
        db: Session,
        study_plan_subject_id: int,
        user_id: int
    ) -> dict:
        rows = (
            db.query(
                StudySession.status,
                func.count(StudySession.id).label("count"),
                func.coalesce(
                    func.sum(StudySession.duration_minutes), 0
                ).label("total_minutes"),
            )
            .join(
                StudyPlanSubject,
                StudyPlanSubject.id == StudySession.study_plan_subject_id
            )
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id
            )
            .filter(
                StudySession.study_plan_subject_id == study_plan_subject_id,
                StudyPlan.user_id == user_id
            )
            .group_by(StudySession.status)
            .all()
        )

        completed_sessions = 0
        pending_sessions = 0
        total_minutes = 0

        for row in rows:
            if row.status == "completed":
                completed_sessions = row.count
                total_minutes = row.total_minutes
            elif row.status == "pending":
                pending_sessions = row.count

        total_sessions = completed_sessions + pending_sessions
        total_hours = round(total_minutes / 60, 2)
        progress_percentage = (
            round(completed_sessions / total_sessions * 100, 2)
            if total_sessions > 0
            else 0.0
        )

        return {
            "study_plan_subject_id": study_plan_subject_id,
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "pending_sessions": pending_sessions,
            "total_minutes": total_minutes,
            "total_hours": total_hours,
            "progress_percentage": progress_percentage,
        }