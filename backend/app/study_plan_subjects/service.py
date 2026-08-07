from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plan_subjects.repository import StudyPlanSubjectRepository


class StudyPlanSubjectService:

    def __init__(self):
        self.repository = StudyPlanSubjectRepository()

    def create(
        self,
        db: Session,
        study_plan_id: int,
        data
    ):
        if data.weekly_hours <= 0:
            raise HTTPException(
                status_code=400,
                detail="Weekly hours must be greater than zero"
            )

        study_plan_subject = StudyPlanSubject(
            study_plan_id=study_plan_id,
            subject_id=data.subject_id,
            weekly_hours=data.weekly_hours,
            created_at=datetime.utcnow()
        )

        return self.repository.create(
            db,
            study_plan_subject
        )

    def list_by_plan(
        self,
        db: Session,
        study_plan_id: int
    ):
        return self.repository.get_by_plan(
            db,
            study_plan_id
        )

    def delete(
        self,
        db: Session,
        study_plan_subject_id: int
    ):
        item = self.repository.get_by_id(
            db,
            study_plan_subject_id
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Study plan subject not found"
            )

        self.repository.delete(
            db,
            item
        )