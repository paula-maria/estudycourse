from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.study_goals.schemas import (
    StudyGoalCreate,
    StudyGoalResponse,
    StudyGoalUpdate,
)
from app.study_goals.service import StudyGoalService

# ajuste este import para o local onde seu get_current_user está
from app.core.security import get_current_user

from app.users.model import User


router = APIRouter(
    prefix="/study-goals",
    tags=["Study Goals"],
)

service = StudyGoalService()


@router.post(
    "",
    response_model=StudyGoalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_goal(
    data: StudyGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db,
        current_user.id,
        data,
    )


@router.get(
    "",
    response_model=list[StudyGoalResponse],
)
def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list(
        db,
        current_user.id,
    )


@router.get(
    "/{study_goal_id}",
    response_model=StudyGoalResponse,
)
def get_goal(
    study_goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get(
        db,
        study_goal_id,
        current_user.id,
    )


@router.put(
    "/{study_goal_id}",
    response_model=StudyGoalResponse,
)
def update_goal(
    study_goal_id: int,
    data: StudyGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update(
        db,
        study_goal_id,
        current_user.id,
        data,
    )


@router.delete(
    "/{study_goal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_goal(
    study_goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db,
        study_goal_id,
        current_user.id,
    )