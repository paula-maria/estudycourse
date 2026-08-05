from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.subjects.schemas import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
)
from app.subjects.service import SubjectService

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)

service = SubjectService()


@router.post(
    "",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db),
):
    return service.create(db, data)


@router.get(
    "",
    response_model=list[SubjectResponse],
)
def list_subjects(
    db: Session = Depends(get_db),
):
    return service.list_all(db)


@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
):
    return service.get_by_id(db, subject_id)


@router.put(
    "/{subject_id}",
    response_model=SubjectResponse,
)
def update_subject(
    subject_id: int,
    data: SubjectUpdate,
    db: Session = Depends(get_db),
):
    return service.update(
        db,
        subject_id,
        data,
    )


@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
):
    service.delete(db, subject_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)