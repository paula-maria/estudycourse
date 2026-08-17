from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.users.model import User
from app.study_plan_subjects.schemas import (
    StudyPlanSubjectCreate,
    StudyPlanSubjectProgress,
    StudyPlanSubjectResponse,
)
from app.study_plan_subjects.service import StudyPlanSubjectService


router = APIRouter(
    prefix="/study-plans",
    tags=["Study Plan Subjects"],
)

service = StudyPlanSubjectService()


@router.post(
    "/{study_plan_id}/subjects",
    response_model=StudyPlanSubjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_subject_to_plan(
    study_plan_id: int,
    data: StudyPlanSubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db,
        study_plan_id,
        data
    )


@router.get(
    "/plan/{study_plan_id}",
    response_model=list[StudyPlanSubjectResponse],
)
def list_by_plan(
    study_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_by_plan(
        db,
        study_plan_id,
        current_user.id
    )


@router.get(
    "/{study_plan_subject_id}",
    response_model=StudyPlanSubjectResponse,
)
def get_study_plan_subject(
    study_plan_subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get(
        db,
        study_plan_subject_id,
        current_user.id
    )


@router.delete(
    "/subjects/{study_plan_subject_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_subject_from_plan(
    study_plan_subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db,
        study_plan_subject_id,
        current_user.id
    )


@router.get(
    "/subjects/{study_plan_subject_id}/progress",
    response_model=StudyPlanSubjectProgress,
)
def get_progress(
    study_plan_subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_progress(
        db,
        study_plan_subject_id,
        current_user.id,
    )