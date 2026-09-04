# StudyCourses

Plataforma inteligente de preparação para concursos públicos.

O StudyCourses tem como objetivo auxiliar estudantes na organização dos estudos através da análise de editais, criação de cronogramas personalizados, acompanhamento de desempenho e geração de cadernos de erros.

A plataforma busca transformar um edital de concurso em uma estratégia de estudos personalizada, considerando o perfil, objetivos, disponibilidade e evolução do estudante.

---

# Objetivo

Criar uma plataforma capaz de:

- interpretar editais de concursos;
- organizar conteúdos cobrados;
- gerar cronogramas personalizados;
- acompanhar o progresso do estudante;
- identificar dificuldades;
- auxiliar na revisão através de cadernos de erros.

---

# Funcionalidades

## Gestão de usuários

- Cadastro de usuários;
- Login;
- Autenticação JWT via Bearer token;
- Perfil do estudante;
- Preferências de estudo;
- Histórico de atividades.

---

## Perfil do estudante

Antes da criação do plano de estudos, o sistema coleta informações sobre o estudante:

- concurso desejado;
- cargo;
- data da prova;
- horas disponíveis por dia;
- disciplinas já estudadas;
- nível de conhecimento;
- dificuldades;
- experiência anterior em concursos.

Essas informações serão utilizadas para personalização do planejamento.

---

# API implementada

A documentação interativa da API está disponível em `http://127.0.0.1:8000/docs` quando a aplicação estiver em execução.

## Usuários e autenticação

- `POST /users/register` cria um usuário;
- `POST /users/login` retorna um JWT;
- `GET /users/me` retorna o usuário autenticado.

Envie o token retornado no login no header `Authorization`:

```text
Bearer <token>
```

## Perfil do estudante

As rotas abaixo exigem autenticação e usam o usuário identificado pelo JWT:

- `POST /profile` cria o perfil do estudante;
- `GET /profile` retorna o perfil do estudante autenticado;
- `PUT /profile` atualiza os campos enviados no perfil.

Cada usuário possui, no máximo, um perfil. O perfil armazena objetivo de estudo, prova, data da prova, horas semanais, dias de estudo, escolaridade, experiência e turno preferido.

## Disciplinas

- `POST /subjects` cria uma disciplina;
- `GET /subjects` lista disciplinas;
- `GET /subjects/{subject_id}` busca uma disciplina;
- `PUT /subjects/{subject_id}` atualiza uma disciplina;
- `DELETE /subjects/{subject_id}` remove uma disciplina.

## Metas de estudo

- `POST /study-goals` cria uma meta de estudos;
- `GET /study-goals` lista as metas do usuário autenticado;
- `GET /study-goals/{study_goal_id}` busca uma meta por ID;
- `PUT /study-goals/{study_goal_id}` atualiza uma meta;
- `DELETE /study-goals/{study_goal_id}` remove uma meta.

---

## Análise de edital

O usuário poderá realizar upload de um edital em PDF.

O sistema deverá:

- extrair texto do documento;
- identificar disciplinas;
- identificar assuntos;
- organizar conteúdos;
- gerar uma estrutura de estudos.

---

## Cronograma inteligente

O sistema cria planos considerando:

- data da prova;
- peso das disciplinas;
- disponibilidade diária;
- dificuldade do estudante;
- progresso realizado.

---

## Checklist de estudos

Controle das atividades:

- conteúdos concluídos;
- revisões pendentes;
- metas diárias;
- progresso geral.

---

## Caderno de erros

Registro das questões que o estudante errou:

- questão;
- disciplina;
- assunto;
- motivo do erro;
- revisão necessária;
- histórico de desempenho.

---

# Tecnologias

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication

## Frontend

- React
- TypeScript
- Tailwind CSS

## Infraestrutura

- Docker
- Docker Compose
- Nginx

## Inteligência Artificial

Planejado:

- processamento de documentos;
- NLP para análise de editais;
- embeddings;
- recomendação personalizada;
- análise de desempenho.

---

# Estrutura atual do backend

```text
backend/
├── alembic/              # migrations e registro dos models
├── app/
│   ├── core/             # configuração, banco, JWT e dependências
│   ├── users/            # cadastro, login e usuário autenticado
│   ├── student_profiles/ # perfil do estudante
│   ├── subjects/         # disciplinas
│   └── main.py           # aplicação e registro dos routers
├── requirements.txt
└── .env                  # configuração local (não versionada)
```

Cada domínio organiza `model.py`, `schemas.py`, `repository.py`, `service.py` e `router.py`. Models SQLAlchemy que devem entrar em migrations precisam ser importados em `alembic/env.py`, para que façam parte de `Base.metadata`.

# Como executar

### 1. Criar ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar ambiente virtual

```bash
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie o arquivo `.env` na pasta `backend`:

```bash
touch .env
```

Exemplo:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/study_platform
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Executar migrations do banco

```bash
python -m alembic upgrade head
```

### 6. Executar aplicação

```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em:

http://127.0.0.1:8000

Documentação automática:

http://127.0.0.1:8000/docs

### 7. Executar testes automatizados

Navegue até a pasta `backend` com o ambiente virtual ativado e execute:

```bash
PYTHONPATH=. pytest
```

