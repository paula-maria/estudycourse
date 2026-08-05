from sqlalchemy.orm import Session

from app.student_profiles.model import StudentProfile


def get_profile_by_user(
    db: Session,
    user_id: int,
):
    return (
        db.query(StudentProfile)
        .filter(StudentProfile.user_id == user_id)
        .first()
    )


def create_profile(
    db: Session,
    profile: StudentProfile,
):
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def update_profile(
    db: Session,
    profile: StudentProfile,
):
    db.commit()
    db.refresh(profile)

    return profile
