"""
Testes automatizados para o módulo de progresso.

Estrutura dos testes:
  SQLite em memória (via conftest.py)
       ↓
  dados de teste criados diretamente via ORM
       ↓
  chamadas à API com TestClient
       ↓
  assertions nos resultados
"""

from datetime import date, datetime

import pytest

from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plans.model import StudyPlan
from app.study_sessions.model import StudySession


# ---------------------------------------------------------------------------
# Helpers para criar dados de teste
# ---------------------------------------------------------------------------


def create_study_plan(db, user_id: int) -> StudyPlan:
    """Cria um plano de estudos para o usuário informado."""
    plan = StudyPlan(
        user_id=user_id,
        title="Plano de Teste",
        description="Plano criado para testes automatizados",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31),
        created_at=datetime.utcnow(),
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def create_study_plan_subject(
    db,
    study_plan_id: int,
    subject_id: int,
    weekly_hours: int = 4,
) -> StudyPlanSubject:
    """Vincula uma matéria a um plano de estudos."""
    sps = StudyPlanSubject(
        study_plan_id=study_plan_id,
        subject_id=subject_id,
        weekly_hours=weekly_hours,
        created_at=datetime.utcnow(),
    )
    db.add(sps)
    db.commit()
    db.refresh(sps)
    return sps


def create_study_session(
    db,
    study_plan_subject_id: int,
    duration_minutes: int,
    status: str,
) -> StudySession:
    """Cria uma sessão de estudo com o status especificado."""
    session = StudySession(
        study_plan_subject_id=study_plan_subject_id,
        session_date=date(2026, 6, 1),
        duration_minutes=duration_minutes,
        status=status,
        created_at=datetime.utcnow(),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


# ---------------------------------------------------------------------------
# Teste 1: acesso sem autenticação deve retornar 401
# ---------------------------------------------------------------------------


def test_get_progress_unauthenticated(client):
    """Endpoint /progress requer JWT — sem token deve retornar 401."""
    response = client.get("/progress")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Teste 2: usuário autenticado sem nenhuma sessão → progresso zerado
# ---------------------------------------------------------------------------


def test_get_progress_empty(client, db_session, user_a, headers_a):
    """Usuário sem nenhuma sessão de estudo deve retornar progresso zerado."""
    response = client.get("/progress", headers=headers_a)

    assert response.status_code == 200

    data = response.json()
    assert data["total_sessions"] == 0
    assert data["completed_sessions"] == 0
    assert data["pending_sessions"] == 0
    assert data["total_minutes"] == 0
    assert data["total_hours"] == 0.0
    assert data["progress_percentage"] == 0.0


# ---------------------------------------------------------------------------
# Teste 3: progresso geral — 3 completed + 2 pending = 60%
# ---------------------------------------------------------------------------


def test_get_progress_with_sessions(
    client, db_session, user_a, subject_1, headers_a
):
    """
    Cenário:
      5 sessões no total
        └── 3 completed  (90 min cada → 270 min totais)
        └── 2 pending    (não contam nos minutos)

    Esperado:
      completed_sessions   = 3
      pending_sessions     = 2
      total_minutes        = 270
      total_hours          = 4.5
      progress_percentage  = 60.0
    """
    plan = create_study_plan(db_session, user_a.id)
    sps = create_study_plan_subject(db_session, plan.id, subject_1.id)

    # 3 sessões completadas — 90 min cada
    for _ in range(3):
        create_study_session(db_session, sps.id, 90, "completed")

    # 2 sessões pendentes — 60 min cada (não entram no total de minutos)
    for _ in range(2):
        create_study_session(db_session, sps.id, 60, "pending")

    response = client.get("/progress", headers=headers_a)

    assert response.status_code == 200

    data = response.json()
    assert data["total_sessions"] == 5
    assert data["completed_sessions"] == 3
    assert data["pending_sessions"] == 2
    assert data["total_minutes"] == 270
    assert data["total_hours"] == 4.5
    assert data["progress_percentage"] == 60.0


# ---------------------------------------------------------------------------
# Teste 4: progresso de um plano específico
# ---------------------------------------------------------------------------


def test_get_plan_progress(
    client, db_session, user_a, subject_1, headers_a
):
    """Progresso filtrado por study_plan_id deve refletir só as sessões daquele plano."""
    plan = create_study_plan(db_session, user_a.id)
    sps = create_study_plan_subject(db_session, plan.id, subject_1.id)

    create_study_session(db_session, sps.id, 60, "completed")
    create_study_session(db_session, sps.id, 60, "completed")
    create_study_session(db_session, sps.id, 30, "pending")

    response = client.get(
        f"/progress/study-plan/{plan.id}",
        headers=headers_a,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total_sessions"] == 3
    assert data["completed_sessions"] == 2
    assert data["pending_sessions"] == 1
    assert data["total_minutes"] == 120
    assert data["total_hours"] == 2.0
    assert data["progress_percentage"] == round(2 / 3 * 100, 2)


# ---------------------------------------------------------------------------
# Teste 5: plano inexistente ou sem sessões retorna 404
# ---------------------------------------------------------------------------


def test_get_plan_progress_not_found(client, headers_a):
    """Plano que não existe (ou sem sessões) deve retornar 404."""
    response = client.get("/progress/study-plan/99999", headers=headers_a)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Teste 6: progresso por matéria
# ---------------------------------------------------------------------------


def test_get_subjects_progress(
    client, db_session, user_a, subject_1, headers_a
):
    """Progresso agrupado por matéria deve retornar a lista correta."""
    plan = create_study_plan(db_session, user_a.id)
    sps = create_study_plan_subject(db_session, plan.id, subject_1.id)

    create_study_session(db_session, sps.id, 45, "completed")
    create_study_session(db_session, sps.id, 45, "pending")

    response = client.get("/progress/subjects", headers=headers_a)

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1

    subject_data = data[0]
    assert subject_data["subject_name"] == "Matemática"
    assert subject_data["total_sessions"] == 2
    assert subject_data["completed_sessions"] == 1
    assert subject_data["pending_sessions"] == 1
    assert subject_data["total_minutes"] == 45
    assert subject_data["progress_percentage"] == 50.0


# ---------------------------------------------------------------------------
# Teste 7: isolamento — usuário B não vê dados do usuário A
# ---------------------------------------------------------------------------


def test_isolation_progress(
    client, db_session, user_a, user_b, subject_1, headers_a, headers_b
):
    """
    Usuário B não deve ver as sessões criadas para o Usuário A.
    """
    # Cria dados para User A
    plan_a = create_study_plan(db_session, user_a.id)
    sps_a = create_study_plan_subject(db_session, plan_a.id, subject_1.id)
    create_study_session(db_session, sps_a.id, 60, "completed")
    create_study_session(db_session, sps_a.id, 60, "completed")

    # User B não tem nenhuma sessão
    response_b = client.get("/progress", headers=headers_b)

    assert response_b.status_code == 200

    data_b = response_b.json()
    assert data_b["total_sessions"] == 0
    assert data_b["completed_sessions"] == 0

    # User A enxerga seus próprios dados
    response_a = client.get("/progress", headers=headers_a)
    data_a = response_a.json()
    assert data_a["total_sessions"] == 2
    assert data_a["completed_sessions"] == 2
