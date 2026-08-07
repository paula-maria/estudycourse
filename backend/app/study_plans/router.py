from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.study_plans.schemas import (
    StudyPlanCreate,
    StudyPlanResponse,
    StudyPlanUpdate,
)
from app.study_plans.service import StudyPlanService


router = APIRouter(
    prefix="/study-plans",
    tags=["Study Plans"],
)

service = StudyPlanService()


@router.post(
    "",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_study_plan(
    data: StudyPlanCreate,
    db: Session = Depends(get_db),
):
    user_id = 1

    return service.create(
        db,
        user_id,
        data
    )


@router.get(
    "",
    response_model=list[StudyPlanResponse],
)
def list_study_plans(
    db: Session = Depends(get_db),
):
    user_id = 1

    return service.list(
        db,
        user_id
    )


@router.get(
    "/{study_plan_id}",
    response_model=StudyPlanResponse,
)
def get_study_plan(
    study_plan_id: int,
    db: Session = Depends(get_db),
):
    user_id = 1

    return service.get(
        db,
        study_plan_id,
        user_id
    )


@router.put(
    "/{study_plan_id}",
    response_model=StudyPlanResponse,
)
def update_study_plan(
    study_plan_id: int,
    data: StudyPlanUpdate,
    db: Session = Depends(get_db),
):
    user_id = 1

    return service.update(
        db,
        study_plan_id,
        user_id,
        data
    )


@router.delete(
    "/{study_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_study_plan(
    study_plan_id: int,
    db: Session = Depends(get_db),
):
    user_id = 1

    service.delete(
        db,
        study_plan_id,
        user_id
    )