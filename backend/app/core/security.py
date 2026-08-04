"""
Funções relacionadas à segurança.

Responsabilidades:

- Criar hash de senha;
- Verificar senha informada pelo usuário;
- Gerar JWT.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Gera hash bcrypt da senha.
    """

    pwd_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(
        pwd_bytes,
        salt
    ).decode("utf-8")



def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Compara senha informada
    com hash salvo.
    """

    plain_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    try:
        return bcrypt.checkpw(
            plain_bytes,
            hashed_bytes
        )

    except ValueError:
        return False



def create_access_token(
    data: dict
) -> str:
    """
    Cria token JWT.

    Exemplo:

    Entrada:

    {
        "sub": "1"
    }

    Saída:

    eyJhbGciOiJIUzI1...
    """

    to_encode = data.copy()


    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


    to_encode.update(
        {
            "exp": expire
        }
    )


    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )