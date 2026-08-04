"""
Funções relacionadas à segurança.

Responsabilidades:

- Criar hash de senha;
- Verificar senha informada pelo usuário;
- Futuramente gerar e validar JWT.
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Recebe uma senha normal e retorna
    uma senha criptografada.

    Exemplo:

    Entrada:
        "123456"

    Saída:
        "$2b$12$8fJ...."

    Essa saída será salva no banco.
    """
    # bcrypt requer bytes
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    # Retorna como string para compatibilidade com o banco
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Compara uma senha digitada pelo usuário
    com o hash salvo no banco.

    Exemplo:

    Usuário digita:

        "123456"

    Banco possui:

        "$2b$12$..."

    Retorna:

        True  -> senha correta
        False -> senha errada
    """
    # bcrypt requer bytes
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    try:
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except ValueError:
        return False