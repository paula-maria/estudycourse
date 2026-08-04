"""
Service de usuários.

Responsabilidade:

- Aplicar regras de negócio;
- Coordenar criação de usuários;
- Usar segurança de senha;
- Chamar repository.

Não faz SQL diretamente.
"""

from sqlalchemy.orm import Session

from app.users import repository
from app.users.model import User
from app.users.schemas import UserCreate
from app.core.security import hash_password
from app.core.security import (
    verify_password,
    create_access_token
)
def login_user(
    db: Session,
    email: str,
    password: str
):
    user = repository.get_user_by_email(
        db,
        email
    )


    if not user:
        raise ValueError(
            "Email ou senha inválidos"
        )


    if not verify_password(
        password,
        user.password_hash
    ):
        raise ValueError(
            "Email ou senha inválidos"
        )


    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }

def create_user(
    db: Session,
    user_data: UserCreate
):
    """
    Cria um novo usuário.

    Fluxo:

    UserCreate
        |
        |
        v
    Verifica email
        |
        |
        v
    Gera password_hash
        |
        |
        v
    Cria Model User
        |
        |
        v
    Repository salva no banco
    """


    # Verifica se já existe usuário
    existing_user = repository.get_user_by_email(
        db,
        user_data.email
    )


    if existing_user:
        raise ValueError(
            "Email já cadastrado"
        )


    # Transformar senha em hash
    password_hash = hash_password(
        user_data.password
    )


    # Criar objeto SQLAlchemy
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash
    )


    # Salvar no banco
    return repository.create_user(
        db,
        new_user
    )