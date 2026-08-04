# StudyFlow AI

StudyFlow AI é uma plataforma inteligente para planejamento e acompanhamento de estudos para concursos públicos.

O sistema utiliza Inteligência Artificial para interpretar editais em PDF, extrair automaticamente disciplinas e conteúdos programáticos, construir um plano de estudos personalizado e acompanhar continuamente a evolução do estudante.

O objetivo da plataforma é atuar como um assistente de estudos, adaptando o cronograma conforme o desempenho, disponibilidade e objetivos de cada usuário.

---

## Principais funcionalidades

- Autenticação de usuários
- Perfil de aprendizagem
- Questionário inicial para conhecer o estudante
- Upload de editais em PDF
- Extração automática de informações do edital
- Organização automática das disciplinas e tópicos
- Geração de cronograma personalizado
- Checklist do conteúdo programático
- Controle de sessões de estudo
- Revisão espaçada
- Caderno de erros
- Banco de questões
- Simulados
- Dashboard de desempenho
- Assistente de estudos baseado em IA

---

## Tecnologias

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis

### Inteligência Artificial

- OpenAI API
- PyMuPDF
- pdfplumber

### Infraestrutura

- Docker
- Docker Compose

---

## Estrutura do projeto

```
studyflow-ai/

├── backend/
├── frontend/
├── docs/
├── docker/
├── scripts/
├── architecture.md
├── README.md
└── LICENSE
```

---

## Fluxo da aplicação

```
Cadastro

↓

Questionário inicial

↓

Upload do edital

↓

Extração do conteúdo

↓

Organização das disciplinas

↓

Plano de estudos

↓

Checklist

↓

Sessões de estudo

↓

Análise de desempenho

↓

Reorganização automática do cronograma
```

---

## Roadmap

### MVP

- Cadastro de usuários
- Login
- Perfil do estudante
- Upload de edital
- Parser de PDF
- Cronograma
- Checklist

### Versão 2

- Questões
- Caderno de erros
- Dashboard
- Revisão espaçada

### Versão 3

- Assistente IA
- Flashcards
- Simulados inteligentes
- Aplicativo mobile

---

## Licença

MIT