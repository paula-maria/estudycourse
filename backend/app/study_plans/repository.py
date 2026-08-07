from sqlalchemy.orm import Session

from app.study_plans.model import StudyPlan


class StudyPlanRepository:

    def create(
        self,
        db: Session,
        study_plan: StudyPlan
    ):
        db.add(study_plan)
        db.commit()
        db.refresh(study_plan)

        return study_plan

    def get_by_id(
        self,
        db: Session,
        study_plan_id: int
    ):
        return (
            db.query(StudyPlan)
            .filter(
                StudyPlan.id == study_plan_id
            )
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int
    ):
        return (
            db.query(StudyPlan)
            .filter(
                StudyPlan.user_id == user_id
            )
            .all()
        )

    def update(
        self,
        db: Session,
        study_plan: StudyPlan
    ):
        db.commit()
        db.refresh(study_plan)

        return study_plan

    def delete(
        self,
        db: Session,
        study_plan: StudyPlan
    ):
        db.delete(study_plan)
        db.commit()