from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.users.model import User

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
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db,
        current_user.id,
        data
    )


@router.get(
    "",
    response_model=list[StudyPlanResponse],
)
def list_study_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list(
        db,
        current_user.id
    )


@router.get(
    "/{study_plan_id}",
    response_model=StudyPlanResponse,
)
def get_study_plan(
    study_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get(
        db,
        study_plan_id,
        current_user.id
    )


@router.put(
    "/{study_plan_id}",
    response_model=StudyPlanResponse,
)
def update_study_plan(
    study_plan_id: int,
    data: StudyPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update(
        db,
        study_plan_id,
        current_user.id,
        data
    )


@router.delete(
    "/{study_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_study_plan(
    study_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db,
        study_plan_id,
        current_user.id
    )