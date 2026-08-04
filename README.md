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
- Autenticação;
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

# Arquitetura inicial
studycourses/

├── backend/
│
│ ├── app/
│ │
│ │ ├── core/
│ │ ├── users/
│ │ ├── exams/
│ │ ├── schedules/
│ │ └── questions/
│ │
│ ├── alembic/
│ ├── requirements.txt
│ └── .env
│
├── frontend/
│
├── docs/
│
└── docker-compose.yml


### 1. Criar ambiente virtual

```bash
python -m venv .venv
2. Ativar ambiente virtual

Linux:

source .venv/bin/activate
3. Instalar dependências
pip install -r requirements.txt
4. Configurar variáveis de ambiente

Criar o arquivo .env na pasta backend:

touch .env

Exemplo:

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/study_platform

SECRET_KEY=sua_chave_secreta

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Executar migrations do banco
python -m alembic upgrade head
6. Executar aplicação
python -m uvicorn app.main:app --reload

A API estará disponível em:

http://127.0.0.1:8000

Documentação automática:

http://127.0.0.1:8000/docs