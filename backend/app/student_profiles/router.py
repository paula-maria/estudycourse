from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.student_profiles import service
from app.student_profiles.schemas import (
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate,
)
from app.users.model import User


router = APIRouter(
    prefix="/profile",
    tags=["Student Profile"],
)


@router.post(
    "",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    profile_data: StudentProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.create_profile(db, current_user.id, profile_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get(
    "",
    response_model=StudentProfileResponse,
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.get_profile(db, current_user.id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put(
    "",
    response_model=StudentProfileResponse,
)
def update_profile(
    profile_data: StudentProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.update_profile(db, current_user.id, profile_data)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
