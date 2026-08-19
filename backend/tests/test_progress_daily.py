import pytest
from datetime import date, datetime, timezone

from app.study_plans.model import StudyPlan
from app.study_plan_subjects.model import StudyPlanSubject
from app.study_sessions.model import StudySession


# ─── helpers ────────────────────────────────────────────────────────────────

def _setup_plan_subject(db_session, user, subject):
    """Cria um StudyPlan + StudyPlanSubject para o usuário e retorna o subject."""
    plan = StudyPlan(
        user_id=user.id,
        title="Plano Teste",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 31),
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(plan)
    db_session.commit()
    db_session.refresh(plan)

    sps = StudyPlanSubject(
        study_plan_id=plan.id,
        subject_id=subject.id,
        weekly_hours=4,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(sps)
    db_session.commit()
    db_session.refresh(sps)

    return sps


def _add_session(db_session, study_plan_subject_id, session_date, duration, status):
    session = StudySession(
        study_plan_subject_id=study_plan_subject_id,
        session_date=session_date,
        duration_minutes=duration,
        status=status,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(session)
    db_session.commit()


# ─── testes ─────────────────────────────────────────────────────────────────

def test_daily_progress_unauthenticated(client):
    """Sem token → 401."""
    response = client.get("/progress/daily")
    assert response.status_code == 401


def test_daily_progress_no_sessions(client, headers_a):
    """Usuário autenticado sem nenhuma sessão → lista vazia."""
    response = client.get("/progress/daily", headers=headers_a)
    assert response.status_code == 200
    assert response.json() == []


def test_daily_progress_with_sessions(client, db_session, headers_a, user_a, subject_1):
    """
    18/08 → 60 completed + 90 completed  → 150 min, 2 sessões
    19/08 → 120 completed + 45 pending   → 120 min, 1 sessão
    pending não entra no tempo nem na contagem.
    """
    sps = _setup_plan_subject(db_session, user_a, subject_1)

    _add_session(db_session, sps.id, date(2026, 8, 18), 60,  "completed")
    _add_session(db_session, sps.id, date(2026, 8, 18), 90,  "completed")
    _add_session(db_session, sps.id, date(2026, 8, 19), 120, "completed")
    _add_session(db_session, sps.id, date(2026, 8, 19), 45,  "pending")

    response = client.get("/progress/daily", headers=headers_a)
    assert response.status_code == 200

    data = {item["date"]: item for item in response.json()}

    assert "2026-08-18" in data
    assert data["2026-08-18"]["minutes_studied"] == 150
    assert data["2026-08-18"]["sessions_completed"] == 2

    assert "2026-08-19" in data
    assert data["2026-08-19"]["minutes_studied"] == 120
    assert data["2026-08-19"]["sessions_completed"] == 1


def test_daily_progress_pending_does_not_count(client, db_session, headers_a, user_a, subject_1):
    """Somente sessões completed entram no cálculo de minutos e contagem."""
    sps = _setup_plan_subject(db_session, user_a, subject_1)

    _add_session(db_session, sps.id, date(2026, 8, 20), 120, "pending")
    _add_session(db_session, sps.id, date(2026, 8, 20), 120, "pending")

    response = client.get("/progress/daily", headers=headers_a)
    assert response.status_code == 200
    assert response.json() == []


def test_daily_progress_isolation(client, db_session, headers_b, user_a, user_b, subject_1):
    """
    User A tem sessões em 18/08.
    User B não deve ver os dados do User A.
    """
    sps = _setup_plan_subject(db_session, user_a, subject_1)

    _add_session(db_session, sps.id, date(2026, 8, 18), 60, "completed")
    _add_session(db_session, sps.id, date(2026, 8, 18), 90, "completed")

    response = client.get("/progress/daily", headers=headers_b)
    assert response.status_code == 200
    assert response.json() == []
