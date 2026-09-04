from datetime import date, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.study_goals.enums import GoalStatus, GoalType
from app.study_goals.model import StudyGoal
from app.study_goals.repository import StudyGoalRepository
from app.study_goals.schemas import (
    StudyGoalCreate,
    StudyGoalResponse,
    StudyGoalUpdate,
)
from app.study_plans.repository import StudyPlanRepository


class StudyGoalService:

    def __init__(self):
        self.repository = StudyGoalRepository()
        self.study_plan_repository = StudyPlanRepository()

    def to_response(
        self,
        study_goal: StudyGoal,
    ) -> StudyGoalResponse:

        return StudyGoalResponse(
            id=study_goal.id,
            user_id=study_goal.user_id,
            study_plan_id=study_goal.study_plan_id,
            title=study_goal.title,
            description=study_goal.description,
            goal_type=study_goal.goal_type,
            target_value=study_goal.target_value,
            current_value=study_goal.current_value,
            start_date=study_goal.start_date,
            end_date=study_goal.end_date,
            status=study_goal.status,
            is_primary=study_goal.is_primary,
            created_at=study_goal.created_at,
            updated_at=study_goal.updated_at,
            progress_percentage=self.calculate_progress(study_goal),
        )

    def _get_goal_or_404(
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

    def create(
        self,
        db: Session,
        user_id: int,
        data: StudyGoalCreate,
    ) -> StudyGoalResponse:

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

        study_goal = self.repository.create(
            db,
            study_goal,
        )

        return self.to_response(study_goal)

    def get(
        self,
        db: Session,
        study_goal_id: int,
        user_id: int,
    ) -> StudyGoalResponse:

        study_goal = self._get_goal_or_404(
            db,
            study_goal_id,
            user_id,
        )

        return self.to_response(study_goal)

    def list(
        self,
        db: Session,
        user_id: int,
    ) -> list[StudyGoalResponse]:

        goals = self.repository.list_by_user(
            db,
            user_id,
        )

        return [
            self.to_response(goal)
            for goal in goals
        ]

    def update(
        self,
        db: Session,
        study_goal_id: int,
        user_id: int,
        data: StudyGoalUpdate,
    ) -> StudyGoalResponse:

        study_goal = self._get_goal_or_404(
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

        study_goal = self.repository.update(
            db,
            study_goal,
        )

        return self.to_response(study_goal)

    def delete(
        self,
        db: Session,
        study_goal_id: int,
        user_id: int,
    ) -> None:

        study_goal = self._get_goal_or_404(
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