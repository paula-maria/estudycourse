from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.progress.schemas import DashboardResponse
from app.progress.service import ProgressService
from app.users.model import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

service = ProgressService()


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_dashboard(
        db,
        current_user.id,
    )
