from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.study_plans.model import StudyPlan
from app.study_plans.repository import StudyPlanRepository


class StudyPlanService:

    def __init__(self):
        self.repository = StudyPlanRepository()

    def create(
        self,
        db: Session,
        user_id: int,
        data
    ):
        if data.end_date <= data.start_date:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date"
            )

        study_plan = StudyPlan(
            user_id=user_id,
            title=data.title,
            description=data.description,
            start_date=data.start_date,
            end_date=data.end_date,
            created_at=datetime.utcnow()
        )

        return self.repository.create(
            db,
            study_plan
        )

    def get(
        self,
        db: Session,
        study_plan_id: int,
        user_id: int
    ):
        study_plan = self.repository.get_by_id(
            db,
            study_plan_id
        )

        if not study_plan:
            raise HTTPException(
                status_code=404,
                detail="Study plan not found"
            )

        if study_plan.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return study_plan

    def list(
        self,
        db: Session,
        user_id: int
    ):
        return self.repository.get_by_user(
            db,
            user_id
        )

    def update(
        self,
        db: Session,
        study_plan_id: int,
        user_id: int,
        data
    ):
        study_plan = self.get(
            db,
            study_plan_id,
            user_id
        )

        values = data.model_dump(
            exclude_unset=True
        )

        new_start = values.get(
            "start_date",
            study_plan.start_date
        )

        new_end = values.get(
            "end_date",
            study_plan.end_date
        )

        if new_end <= new_start:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date"
            )

        for field, value in values.items():
            setattr(
                study_plan,
                field,
                value
            )

        return self.repository.update(
            db,
            study_plan
        )

    def delete(
        self,
        db: Session,
        study_plan_id: int,
        user_id: int
    ):
        study_plan = self.get(
            db,
            study_plan_id,
            user_id
        )

        self.repository.delete(
            db,
            study_plan
        )