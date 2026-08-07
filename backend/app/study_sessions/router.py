from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.study_sessions.schemas import (
    StudySessionCreate,
    StudySessionResponse,
    StudySessionUpdate,
)
from app.study_sessions.service import StudySessionService


router = APIRouter(
    prefix="/study-sessions",
    tags=["Study Sessions"],
)

service = StudySessionService()


@router.post(
    "",
    response_model=StudySessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    data: StudySessionCreate,
    db: Session = Depends(get_db),
):
    return service.create(
        db,
        data
    )


@router.get(
    "/{session_id}",
    response_model=StudySessionResponse,
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    return service.get(
        db,
        session_id
    )


@router.get(
    "/plan-subject/{study_plan_subject_id}",
    response_model=list[StudySessionResponse],
)
def list_sessions(
    study_plan_subject_id: int,
    db: Session = Depends(get_db),
):
    return service.list_by_plan_subject(
        db,
        study_plan_subject_id
    )


@router.put(
    "/{session_id}",
    response_model=StudySessionResponse,
)
def update_session(
    session_id: int,
    data: StudySessionUpdate,
    db: Session = Depends(get_db),
):
    return service.update(
        db,
        session_id,
        data
    )


@router.patch(
    "/{session_id}/complete",
    response_model=StudySessionResponse,
)
def complete_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    return service.complete(
        db,
        session_id
    )


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    service.delete(
        db,
        session_id
    )