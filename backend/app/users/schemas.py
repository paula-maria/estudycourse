"""Este arquivo define os modelos de entrada e saída
Eles NÃO representam tabelas do banco.

Fluxo:

Request HTTP
     |
     v
Schema Pydantic
     |
     v
Service
     |
     v
SQLAlchemy Model
     |
     v
PostgreSQL
"""

from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

# CADASTRO DE USUÁRIO
# Endpoint futuro:
#
# POST /register
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# LOGIN DO USUÁRIO
# Endpoint futuro:
# POST /login
# Responsabilidade:
# Receber credenciais para autenticação.
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# RESPOSTA DA API
# Usado nos endpoints:
# POST /register
# GET /me
# Representa os dados públicos
# que podem retornar para o frontend.
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    # Permite que o Pydantic leia objetos
    # vindos do SQLAlchemy.
    class Config:
        from_attributes = True

# USUÁRIO ATUAL
# Endpoint futuro:
# GET /me
# Responsabilidade:
# Retornar os dados do usuário autenticado
# através do JWT.