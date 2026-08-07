from sqlalchemy.orm import Session

from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plans.model import StudyPlan


class StudyPlanSubjectRepository:

    def create(
        self,
        db: Session,
        study_plan_subject: StudyPlanSubject
    ):
        db.add(study_plan_subject)
        db.commit()
        db.refresh(study_plan_subject)

        return study_plan_subject

    def get_by_id(
        self,
        db: Session,
        study_plan_subject_id: int
    ):
        return (
            db.query(StudyPlanSubject)
            .filter(
                StudyPlanSubject.id == study_plan_subject_id
            )
            .first()
        )

    def get_by_id_for_user(
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

    def list_by_plan(
        self,
        db: Session,
        study_plan_id: int,
        user_id: int
    ):
        return (
            db.query(StudyPlanSubject)
            .join(
                StudyPlan,
                StudyPlan.id == StudyPlanSubject.study_plan_id
            )
            .filter(
                StudyPlanSubject.study_plan_id == study_plan_id,
                StudyPlan.user_id == user_id
            )
            .all()
        )

    def delete(
        self,
        db: Session,
        study_plan_subject: StudyPlanSubject
    ):
        db.delete(study_plan_subject)
        db.commit()

        