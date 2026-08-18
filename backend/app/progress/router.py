from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.progress.schemas import (
    ProgressResponse,
    SubjectProgressResponse,
)
from app.progress.service import ProgressService
from app.users.model import User


router = APIRouter(
    prefix="/progress",
    tags=["Progress"],
)

service = ProgressService()


@router.get(
    "",
    response_model=ProgressResponse,
)
def get_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_user_progress(
        db,
        current_user.id,
    )


@router.get(
    "/study-plan/{study_plan_id}",
    response_model=ProgressResponse,
)
def get_study_plan_progress(
    study_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_plan_progress(
        db,
        study_plan_id,
        current_user.id,
    )


@router.get(
    "/subjects",
    response_model=list[SubjectProgressResponse],
)
def get_subjects_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_subjects_progress(
        db,
        current_user.id,
    )