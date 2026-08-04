"""
Dependências de autenticação.

Responsabilidades:

- Ler o header Authorization;
- Validar JWT;
- Recuperar usuário logado.

Uso nas rotas:

    @router.get("/me")
    def get_me(
        current_user: User = Depends(get_current_user)
    ):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.users import repository
from app.users.model import User


# HTTPBearer exibe um campo simples no Swagger
# para colar o token JWT diretamente.
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependência que valida o JWT e retorna
    o usuário autenticado.

    Fluxo:

    Header Authorization: Bearer <token>
        |
        v
    Decodifica JWT
        |
        v
    Extrai user_id do campo "sub"
        |
        v
    Busca usuário no banco
        |
        v
    Retorna usuário

    Lança HTTPException 401 se:

    - Token ausente ou malformado;
    - Token expirado;
    - Usuário não encontrado.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = repository.get_user_by_id(
        db,
        int(user_id)
    )

    if user is None:
        raise credentials_exception

    return user
