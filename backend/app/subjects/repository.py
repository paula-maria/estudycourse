from sqlalchemy.orm import Session

from app.subjects.model import Subject
from app.subjects.schemas import SubjectCreate, SubjectUpdate


class SubjectRepository:

    def create(
        self,
        db: Session,
        data: SubjectCreate
    ) -> Subject:

        subject = Subject(**data.model_dump())

        db.add(subject)
        db.commit()
        db.refresh(subject)

        return subject

    def list_all(
        self,
        db: Session
    ) -> list[Subject]:

        return db.query(Subject).order_by(Subject.name).all()

    def get_by_id(
        self,
        db: Session,
        subject_id: int
    ) -> Subject | None:

        return (
            db.query(Subject)
            .filter(Subject.id == subject_id)
            .first()
        )

    def update(
        self,
        db: Session,
        subject: Subject,
        data: SubjectUpdate
    ) -> Subject:

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(subject, key, value)

        db.commit()
        db.refresh(subject)

        return subject

    def delete(
        self,
        db: Session,
        subject: Subject
    ) -> None:

        db.delete(subject)
        db.commit()