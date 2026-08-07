from sqlalchemy.orm import Session

from app.study_sessions.model import StudySession


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

    def get_by_id(
        self,
        db: Session,
        session_id: int
    ):
        return (
            db.query(StudySession)
            .filter(
                StudySession.id == session_id
            )
            .first()
        )

    def get_by_plan_subject(
        self,
        db: Session,
        study_plan_subject_id: int
    ):
        return (
            db.query(StudySession)
            .filter(
                StudySession.study_plan_subject_id
                == study_plan_subject_id
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