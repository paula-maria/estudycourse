# Arquitetura

## Visão Geral

---

# Arquitetura Geral

```
                 Next.js

                     │

               REST API

                     │

                 FastAPI

 ┌────────────┬──────────────┬───────────────┐

 Authentication   Planner   AI   Parser PDF

                     │

              PostgreSQL

                     │

                  Redis
```

---

# Fluxo principal

```
Usuário

↓

Cadastro

↓

Questionário inicial

↓

Perfil do estudante

↓

Upload do edital

↓

Parser

↓

Extração das disciplinas

↓

Plano de estudos

↓

Sessões

↓

Dashboard

↓

Ajuste automático do cronograma
```
---
                Next.js

                    │

            REST API

                    │

               FastAPI

 ┌──────────┬─────────────┬────────────┐

Auth     Planner     AI      Parser

            │

      PostgreSQL

            │

          Redis
---

# Organização atual do Backend

```
backend/
├── alembic/
│   └── env.py
└── app/
    ├── core/
    │   ├── config.py
    │   ├── database.py
    │   ├── dependencies.py
    │   └── security.py
    ├── users/
    ├── student_profiles/
    ├── subjects/
    └── main.py
```

Cada domínio possui sua própria camada de serviços, repositórios, modelos e schemas.

- `model.py`: mapeamento SQLAlchemy;
- `schemas.py`: contratos de entrada e saída da API;
- `repository.py`: acesso ao banco com SQLAlchemy;
- `service.py`: regras de negócio;
- `router.py`: endpoints FastAPI.

Os models usados em migrations são importados em `alembic/env.py`, permitindo que o Alembic os encontre em `Base.metadata` durante o autogenerate.

---

# Organização do Frontend

```
frontend/

app/

components/

features/

hooks/

services/

types/

styles/

public/
```

O frontend é organizado por funcionalidades, evitando estrutura baseada apenas em componentes.

---

# Módulos

## Authentication

Responsável por autenticação, autorização, gerenciamento de usuários e sessões.

O login gera um JWT contendo o identificador do usuário no campo `sub`. A dependência `get_current_user` recebe o Bearer token, valida e decodifica o JWT, busca o usuário no banco e o fornece às rotas protegidas.

---

## User Profile

Armazena informações do estudante.

- objetivo
- disponibilidade
- rotina
- experiência
- disciplinas fortes
- disciplinas fracas
- preferências de estudo

Na implementação atual, a relação entre `users` e `student_profiles` é 1:1. As rotas `POST /profile`, `GET /profile` e `PUT /profile` exigem autenticação.

---

## Subjects

Gerencia as disciplinas cadastradas na plataforma, com operações de criação, listagem, consulta, atualização e remoção pela rota `/subjects`.

---

## Diagnostic

Executa uma entrevista inicial para construir o perfil do estudante.

As respostas são utilizadas na geração do primeiro cronograma.

---

## Exam Notice Parser

Responsável pelo processamento dos editais.

Fluxo:

```
PDF

↓

Extração do texto

↓

Limpeza

↓

Identificação da estrutura

↓

IA

↓

JSON estruturado
```

Exemplo:

```json
{
  "disciplina": "Português",
  "topicos": [
    "Pontuação",
    "Concordância",
    "Crase"
  ]
}
```

---

## Planner

Responsável pela geração do cronograma.

O algoritmo considera:

- data da prova
- horas disponíveis
- dificuldade das disciplinas
- desempenho do estudante
- revisões pendentes
- prioridade das matérias

---

## Study

Controla todas as sessões de estudo.

Cada sessão registra:

- início
- término
- assunto
- duração
- produtividade

---

## Checklist

Cada tópico identificado no edital torna-se um item de acompanhamento.

O progresso é calculado automaticamente.

---

## Progress

Módulo responsável por calcular estatísticas de evolução do estudante.

Agrega os dados de sessões concluídas e pendentes (via banco de dados) para apresentar:
- O percentual de conclusão geral.
- O percentual de conclusão por plano de estudos.
- O percentual e total de minutos dedicados agrupados por matéria (disciplina).

---

## Questions

Gerencia banco de questões, simulados e estatísticas.

---

## Mistake Notebook

Armazena automaticamente questões respondidas incorretamente.

Cada registro contém:

- questão
- assunto
- motivo do erro
- observações
- próxima revisão

---

## Dashboard

Centraliza indicadores como:

- horas estudadas
- evolução semanal
- percentual do edital concluído
- disciplinas mais estudadas
- desempenho por assunto

---

## AI Module

Responsável por:

- interpretar editais
- responder dúvidas
- explicar conteúdos
- gerar resumos
- reorganizar cronogramas
- produzir recomendações personalizadas

A comunicação com o modelo de linguagem ocorre através de uma camada de serviço dedicada, desacoplando a aplicação do provedor utilizado.

---

# Banco de Dados

Principais entidades:

```
users
student_profiles
exam_notices
subjects
topics
study_plans
study_sessions
reviews
questions
mistakes
flashcards
simulations
statistics
uploads
```

---

# Escalabilidade

A arquitetura foi projetada para permitir futura separação dos seguintes módulos em serviços independentes:

- Authentication
- AI
- Parser
- Planner
- Notifications

Sem alterações significativas nas demais camadas da aplicação.

---

# Decisões arquiteturais

- Monólito modular para reduzir complexidade inicial.
- FastAPI devido à integração com bibliotecas de IA e processamento de documentos.
- PostgreSQL como banco principal.
- Redis para cache e processamento assíncrono.
- Next.js para frontend.
- Docker para padronização do ambiente de desenvolvimento.
