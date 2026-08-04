from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.users import service
from app.users.model import User
from app.users.schemas import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return service.create_user(
            db,
            user
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.post(
    "/login",
    response_model=Token
)
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):

    try:
        return service.login_user(
            db,
            data.email,
            data.password
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Retorna os dados do usuário autenticado.

    Requer token JWT válido no header:

        Authorization: Bearer <token>
    """

    return current_user