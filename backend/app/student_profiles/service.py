from sqlalchemy.orm import Session

from app.student_profiles import repository
from app.student_profiles.model import StudentProfile
from app.student_profiles.schemas import (
    StudentProfileCreate,
    StudentProfileUpdate,
)


def get_profile(
    db: Session,
    user_id: int,
):
    profile = repository.get_profile_by_user(db, user_id)

    if not profile:
        raise ValueError("Perfil não encontrado")

    return profile


def create_profile(
    db: Session,
    user_id: int,
    profile_data: StudentProfileCreate,
):
    existing_profile = repository.get_profile_by_user(db, user_id)

    if existing_profile:
        raise ValueError("Usuário já possui perfil")

    profile = StudentProfile(
        user_id=user_id,
        **profile_data.model_dump(),
    )

    return repository.create_profile(db, profile)


def update_profile(
    db: Session,
    user_id: int,
    profile_data: StudentProfileUpdate,
):
    profile = get_profile(db, user_id)

    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    return repository.update_profile(db, profile)
