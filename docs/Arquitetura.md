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

# Organização do Backend

```
backend/

app/

├── api/
├── core/
├── models/
├── schemas/
├── repositories/
├── services/
├── workers/
├── tests/
└── main.py
```

Cada domínio possui sua própria camada de serviços, repositórios, modelos e schemas.

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
profiles
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