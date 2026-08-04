"""
Repository de usuários.

Responsabilidade:

- Fazer consultas no banco;
- Criar usuários;
- Buscar usuários existentes.

Não contém regras de negócio.
"""

from sqlalchemy.orm import Session

from app.users.model import User


def get_user_by_email(
    db: Session,
    email: str
):
    """
    Busca um usuário pelo email.

    Usado para:

    - verificar se email já existe;
    - autenticação no login.
    """

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int
):
    """
    Busca um usuário pelo id.

    Usado para:

    - recuperar usuário autenticado via JWT.
    """

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

def create_user(
    db: Session,
    user: User
):
    """
    Salva um usuário no banco.

    Recebe:

    User(
        name,
        email,
        password_hash
    )

    Executa:

    INSERT INTO users

    Retorna:

    usuário criado com id.
    """

    db.add(user)

    db.commit()

    db.refresh(user)

    return user