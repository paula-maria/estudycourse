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