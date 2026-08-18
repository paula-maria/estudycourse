from sqlalchemy import func
from sqlalchemy.orm import Session

from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plans.model import StudyPlan
from app.study_sessions.model import StudySession
from app.subjects.model import Subject


class ProgressRepository:

    def get_user_sessions(self, db: Session, user_id: int):
        return (
            db.query(StudySession)
            .join(
                StudyPlanSubject,
                StudyPlanSubject.id == StudySession.study_plan_subject_id,
            )
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id,
            )
            .filter(
                StudyPlan.user_id == user_id,
            )
            .all()
        )

    def get_plan_sessions(
        self,
        db: Session,
        study_plan_id: int,
        user_id: int,
    ):
        return (
            db.query(StudySession)
            .join(
                StudyPlanSubject,
                StudyPlanSubject.id == StudySession.study_plan_subject_id,
            )
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id,
            )
            .filter(
                StudyPlan.id == study_plan_id,
                StudyPlan.user_id == user_id,
            )
            .all()
        )

    def get_subject_progress(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(
                StudyPlanSubject.id,
                Subject.name.label("subject_name"),
                func.count(StudySession.id).label("total_sessions"),
                func.count(StudySession.id)
                .filter(StudySession.status == "completed")
                .label("completed_sessions"),
                func.sum(StudySession.duration_minutes)
                .filter(StudySession.status == "completed")
                .label("total_minutes"),
            )
            .join(
                Subject,
                Subject.id == StudyPlanSubject.subject_id,
            )
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id,
            )
            .outerjoin(
                StudySession,
                StudySession.study_plan_subject_id == StudyPlanSubject.id,
            )
            .filter(
                StudyPlan.user_id == user_id,
            )
            .group_by(
                StudyPlanSubject.id,
                Subject.name,
            )
            .all()
        )

    def get_daily_progress(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(
                func.date(StudySession.session_date).label("date"),
                func.sum(StudySession.duration_minutes).label("minutes_studied"),
                func.count(StudySession.id).label("sessions_completed"),
            )
            .join(
                StudyPlanSubject,
                StudyPlanSubject.id == StudySession.study_plan_subject_id,
            )
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id,
            )
            .filter(
                StudyPlan.user_id == user_id,
                StudySession.status == "completed",
            )
            .group_by(
                func.date(StudySession.session_date),
            )
            .order_by(
                func.date(StudySession.session_date).asc(),
            )
            .all()
        )