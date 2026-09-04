from datetime import date, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.study_goals.enums import GoalStatus, GoalType
from app.study_goals.model import StudyGoal
from app.study_goals.repository import StudyGoalRepository
from app.study_goals.schemas import StudyGoalCreate, StudyGoalUpdate
from app.study_plans.repository import StudyPlanRepository


class StudyGoalService:

    def __init__(self):
        self.repository = StudyGoalRepository()
        self.study_plan_repository = StudyPlanRepository()

    def create(
        self,
        db: Session,
        user_id: int,
        data: StudyGoalCreate,
    ) -> StudyGoal:

        self._validate_dates(
            data.start_date,
            data.end_date,
        )

        self._validate_study_plan(
            db,
            data.study_plan_id,
            user_id,
        )

        if data.is_primary:
            self._remove_current_primary(
                db,
                user_id,
            )

        study_goal = StudyGoal(
            user_id=user_id,
            study_plan_id=data.study_plan_id,
            title=data.title,
            description=data.description,
            goal_type=data.goal_type,
            target_value=data.target_value,
            current_value=0,
            start_date=data.start_date,
            end_date=data.end_date,
            status=GoalStatus.ACTIVE,
            is_primary=data.is_primary,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        return self.repository.create(
            db,
            study_goal,
        )

    def get(
        self,
        db: Session,
        study_goal_id: int,
        user_id: int,
    ) -> StudyGoal:

        study_goal = self.repository.get_by_id(
            db,
            study_goal_id,
            user_id,
        )

        if not study_goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study goal not found",
            )

        return study_goal

    def list(
        self,
        db: Session,
        user_id: int,
    ) -> list[StudyGoal]:

        return self.repository.list_by_user(
            db,
            user_id,
        )

    def update(
        self,
        db: Session,
        study_goal_id: int,
        user_id: int,
        data: StudyGoalUpdate,
    ) -> StudyGoal:

        study_goal = self.get(
            db,
            study_goal_id,
            user_id,
        )

        if data.study_plan_id is not None:
            self._validate_study_plan(
                db,
                data.study_plan_id,
                user_id,
            )

        if data.start_date is not None or data.end_date is not None:

            start_date = (
                data.start_date
                if data.start_date is not None
                else study_goal.start_date
            )

            end_date = (
                data.end_date
                if data.end_date is not None
                else study_goal.end_date
            )

            self._validate_dates(
                start_date,
                end_date,
            )

        if data.is_primary is True:
            self._remove_current_primary(
                db,
                user_id,
                exclude_id=study_goal.id,
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                study_goal,
                field,
                value,
            )

        study_goal.updated_at = datetime.utcnow()

        return self.repository.update(
            db,
            study_goal,
        )

    def delete(
        self,
        db: Session,
        study_goal_id: int,
        user_id: int,
    ) -> None:

        study_goal = self.get(
            db,
            study_goal_id,
            user_id,
        )

        self.repository.delete(
            db,
            study_goal,
        )

    def calculate_progress(
        self,
        study_goal: StudyGoal,
    ) -> float:

        return study_goal.progress_percentage

    def _validate_study_plan(
        self,
        db: Session,
        study_plan_id: int | None,
        user_id: int,
    ) -> None:

        if study_plan_id is not None:
            study_plan = self.study_plan_repository.get_by_id(
                db,
                study_plan_id,
            )

            if not study_plan or study_plan.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Study plan not found",
                )

    def _validate_dates(
        self,
        start_date: date,
        end_date: date | None,
    ) -> None:

        if end_date is not None and end_date < start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date cannot be before start date",
            )

    def _remove_current_primary(
        self,
        db: Session,
        user_id: int,
        exclude_id: int | None = None,
    ) -> None:

        goals = self.repository.list_by_user(
            db,
            user_id,
        )

        for goal in goals:

            if (
                goal.is_primary
                and goal.id != exclude_id
                and goal.status == GoalStatus.ACTIVE
            ):
                goal.is_primary = False
                goal.updated_at = datetime.utcnow()

        db.flush()