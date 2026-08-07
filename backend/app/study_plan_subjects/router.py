from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.study_plan_subjects.schemas import (
    StudyPlanSubjectCreate,
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
):
    return service.create(
        db,
        study_plan_id,
        data
    )


@router.get(
    "/{study_plan_id}/subjects",
    response_model=list[StudyPlanSubjectResponse],
)
def list_plan_subjects(
    study_plan_id: int,
    db: Session = Depends(get_db),
):
    return service.list_by_plan(
        db,
        study_plan_id
    )


@router.delete(
    "/subjects/{study_plan_subject_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_subject_from_plan(
    study_plan_subject_id: int,
    db: Session = Depends(get_db),
):
    service.delete(
        db,
        study_plan_subject_id
    )