from sqlalchemy import select
from sqlalchemy.orm import Session

from app.study_goals.model import StudyGoal


class StudyGoalRepository:

    def create(
        self,
        db: Session,
        study_goal: StudyGoal,
    ) -> StudyGoal:
        db.add(study_goal)
        db.commit()
        db.refresh(study_goal)

        return study_goal

    def get_by_id(
        self,
        db: Session,
        study_goal_id: int,
        user_id: int,
    ) -> StudyGoal | None:
        statement = (
            select(StudyGoal)
            .where(
                StudyGoal.id == study_goal_id,
                StudyGoal.user_id == user_id,
            )
        )

        return db.scalars(statement).first()

    def list_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[StudyGoal]:
        statement = (
            select(StudyGoal)
            .where(
                StudyGoal.user_id == user_id,
            )
            .order_by(StudyGoal.created_at.desc())
        )

        return list(db.scalars(statement).all())

    def update(
        self,
        db: Session,
        study_goal: StudyGoal,
    ) -> StudyGoal:
        db.commit()
        db.refresh(study_goal)

        return study_goal

    def delete(
        self,
        db: Session,
        study_goal: StudyGoal,
    ) -> None:
        db.delete(study_goal)
        db.commit()
