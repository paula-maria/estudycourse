# eStudyCourse API Documentation

Esta documentação descreve todos os endpoints disponíveis na API do backend do projeto, assim como os requisitos de autenticação.

## Autenticação (JWT)

A maioria dos endpoints da aplicação são protegidos por JWT. Para acessá-los, você deve enviar o token gerado no Header da requisição HTTP:
```
Authorization: Bearer <seu_token_jwt>
```

---

## 1. Users & Auth (`/users`)

Responsável pelo cadastro de usuários e obtenção de token.

- **`POST /users/register`**: Registra um novo usuário no sistema.
  - **Body**: `{"name": "...", "email": "...", "password": "..."}`
  - **Response (201)**: Retorna os dados básicos do usuário (sem senha).
- **`POST /users/login`**: Realiza o login do usuário.
  - **Body**: `{"email": "...", "password": "..."}`
  - **Response (200)**: Retorna o token de acesso: `{"access_token": "...", "token_type": "bearer"}`
- **`GET /users/me`** (Protegido): Obtém os dados do usuário autenticado.

---

## 2. Subjects (`/subjects`)

Gestão global de matérias disponíveis para estudo (Matemática, História, etc).

- **`GET /subjects`**: Lista as matérias disponíveis.
- **`POST /subjects`** (Protegido): Cadastra uma nova matéria base.
- **`GET /subjects/{id}`**: Detalhes de uma matéria específica.

---

## 3. Study Plans (`/study-plans`)

Gerencia os Planos de Estudo **isolados por usuário**. Usuários só conseguem interagir com os planos criados por eles mesmos.

- **`POST /study-plans`** (Protegido): Cria um plano de estudos.
  - **Body**: `{"title": "...", "description": "...", "start_date": "...", "end_date": "..."}`
- **`GET /study-plans`** (Protegido): Lista os planos do usuário autenticado.
- **`GET /study-plans/{id}`** (Protegido): Obtém detalhes de um plano. Retorna 404/403 se pertencer a outro usuário.
- **`PUT /study-plans/{id}`** (Protegido): Atualiza os dados de um plano.
- **`DELETE /study-plans/{id}`** (Protegido): Remove o plano do usuário.

---

## 4. Study Plan Subjects (`/study-plans`)

Associa as matérias globais (`Subject`) aos planos de estudo criados, determinando a carga horária semanal.

- **`POST /study-plans/{study_plan_id}/subjects`** (Protegido): Vincula uma matéria a um plano de estudos específico.
  - **Body**: `{"subject_id": 1, "weekly_hours": 5}`
- **`GET /study-plans/plan/{study_plan_id}`** (Protegido): Lista todas as matérias associadas a um plano de estudos.
- **`GET /study-plans/{study_plan_subject_id}`** (Protegido): Obtém detalhes sobre a associação daquela matéria.
- **`DELETE /study-plans/subjects/{study_plan_subject_id}`** (Protegido): Remove a matéria de um plano de estudos (valida a propriedade do plano com segurança).

---

## 5. Study Sessions (`/study-sessions`)

Agenda e controla sessões de estudo diárias/práticas de uma matéria dentro de um plano.

- **`POST /study-sessions`** (Protegido): Registra uma nova sessão pendente.
  - **Body**: `{"study_plan_subject_id": 1, "session_date": "2026-08-05", "duration_minutes": 60}`
  - *Garante que o `study_plan_subject_id` pertence ao usuário logado.*
- **`GET /study-sessions/plan-subject/{study_plan_subject_id}`** (Protegido): Lista as sessões de uma matéria do plano.
- **`GET /study-sessions/{session_id}`** (Protegido): Consulta a sessão de estudo.
- **`PUT /study-sessions/{session_id}`** (Protegido): Atualiza tempo ou data de uma sessão.
- **`PATCH /study-sessions/{session_id}/complete`** (Protegido): Marca a sessão como concluída (`status = completed`).
- **`DELETE /study-sessions/{session_id}`** (Protegido): Remove a sessão.

---

## 6. Progress (`/progress`)

Gerencia o cálculo e retorno do progresso dos estudos do usuário baseando-se no tempo (minutos) e na quantidade de sessões (concluídas vs. pendentes).

- **`GET /progress`** (Protegido): Retorna o progresso geral do usuário (todas as sessões associadas aos seus planos).
- **`GET /progress/study-plan/{study_plan_id}`** (Protegido): Retorna o progresso filtrado por um plano de estudos específico.
- **`GET /progress/subjects`** (Protegido): Retorna o progresso agrupado por matéria, listando a performance em cada uma.

---

## 7. Health Check (`/`)

- **`GET /`**: Rota raiz de saúde para validar se a API e o banco de dados estão conectados corretamente. Retorna `{"message": "API is running", "database": "connected"}`.

> (Protegido) = Rota protegida por autenticação JWT (requer usuário logado).

