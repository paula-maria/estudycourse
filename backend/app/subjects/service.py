from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.subjects.repository import SubjectRepository
from app.subjects.schemas import SubjectCreate, SubjectUpdate


class SubjectService:

    def __init__(self):
        self.repository = SubjectRepository()

    def create(
        self,
        db: Session,
        data: SubjectCreate
    ):
        subjects = self.repository.list_all(db)

        for subject in subjects:
            if subject.name.lower() == data.name.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Matéria já cadastrada"
                )

        return self.repository.create(db, data)

    def list_all(
        self,
        db: Session
    ):
        return self.repository.list_all(db)

    def get_by_id(
        self,
        db: Session,
        subject_id: int
    ):
        subject = self.repository.get_by_id(db, subject_id)

        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Matéria não encontrada"
            )

        return subject

    def update(
        self,
        db: Session,
        subject_id: int,
        data: SubjectUpdate
    ):
        subject = self.get_by_id(db, subject_id)

        return self.repository.update(
            db,
            subject,
            data
        )

    def delete(
        self,
        db: Session,
        subject_id: int
    ):
        subject = self.get_by_id(db, subject_id)

        self.repository.delete(
            db,
            subject
        )