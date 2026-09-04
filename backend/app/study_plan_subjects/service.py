from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plan_subjects.repository import StudyPlanSubjectRepository
from app.study_sessions.repository import StudySessionRepository


class StudyPlanSubjectService:

    def __init__(self):
        self.repository = StudyPlanSubjectRepository()
        self.session_repository = StudySessionRepository()

    def create(
        self,
        db: Session,
        study_plan_id: int,
        data
    ):
        if data.weekly_hours <= 0:
            raise HTTPException(
                status_code=400,
                detail="A carga horária semanal deve ser maior que zero"
            )

        study_plan_subject = StudyPlanSubject(
            study_plan_id=study_plan_id,
            subject_id=data.subject_id,
            weekly_hours=data.weekly_hours,
            created_at=datetime.utcnow()
        )

        return self.repository.create(
            db,
            study_plan_subject
        )

    def get(
        self,
        db: Session,
        study_plan_subject_id: int,
        user_id: int
    ):
        item = self.repository.get_by_id_for_user(
            db,
            study_plan_subject_id,
            user_id
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Assunto do plano de estudos não encontrado"
            )

        return item

    def list_by_plan(
        self,
        db: Session,
        study_plan_id: int,
        user_id: int
    ):
        return self.repository.list_by_plan(
            db,
            study_plan_id,
            user_id
        )

    def delete(
        self,
        db: Session,
        study_plan_subject_id: int,
        user_id: int
    ):
        item = self.repository.get_by_id_for_user(
            db,
            study_plan_subject_id,
            user_id
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Assunto do plano de estudos não encontrado"
            )

        self.repository.delete(
            db,
            item
        )

    def get_progress(
        self,
        db: Session,
        study_plan_subject_id: int,
        user_id: int
    ):
        item = self.repository.get_by_id_for_user(
            db,
            study_plan_subject_id,
            user_id
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Assunto do plano de estudos não encontrado"
            )

        return self.session_repository.get_progress(
            db,
            study_plan_subject_id,
            user_id
        )