from datetime import date, datetime, timezone

from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plans.model import StudyPlan
from app.study_sessions.model import StudySession


def _now():
    return datetime.now(timezone.utc)


def test_dashboard_unauthenticated(client):
    """Sem token → 401."""
    response = client.get("/progress/dashboard")
    assert response.status_code == 401


def test_dashboard_empty(client, headers_a):
    """Usuário sem sessões → summary zerado, listas vazias."""
    response = client.get("/progress/dashboard", headers=headers_a)
    assert response.status_code == 200

    data = response.json()
    assert "summary" in data
    assert "subjects" in data
    assert "daily_progress" in data

    summary = data["summary"]
    assert summary["total_sessions"] == 0
    assert summary["completed_sessions"] == 0
    assert summary["pending_sessions"] == 0
    assert summary["total_minutes"] == 0
    assert summary["total_hours"] == 0.0
    assert summary["progress_percentage"] == 0.0

    assert data["subjects"] == []
    assert data["daily_progress"] == []


def test_dashboard_with_sessions(
    client, db_session, user_a, subject_1, headers_a
):
    """
    2 sessões completed (60 + 120 min) + 1 pending (45 min).

    summary:
      total_sessions      = 3
      completed_sessions  = 2
      pending_sessions    = 1
      total_minutes       = 180
      total_hours         = 3.0
      progress_percentage = 66.67

    subjects: 1 entrada — Matemática
    daily_progress: 2 entradas (18/08 e 19/08), pending do 20/08 não aparece
    """
    plan = StudyPlan(
        user_id=user_a.id,
        title="Dashboard Plan",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 31),
        created_at=_now(),
    )
    db_session.add(plan)
    db_session.commit()
    db_session.refresh(plan)

    sps = StudyPlanSubject(
        study_plan_id=plan.id,
        subject_id=subject_1.id,
        weekly_hours=4,
        created_at=_now(),
    )
    db_session.add(sps)
    db_session.commit()
    db_session.refresh(sps)

    db_session.add_all([
        StudySession(
            study_plan_subject_id=sps.id,
            session_date=date(2026, 8, 18),
            duration_minutes=60,
            status="completed",
            created_at=_now(),
        ),
        StudySession(
            study_plan_subject_id=sps.id,
            session_date=date(2026, 8, 19),
            duration_minutes=120,
            status="completed",
            created_at=_now(),
        ),
        StudySession(
            study_plan_subject_id=sps.id,
            session_date=date(2026, 8, 20),
            duration_minutes=45,
            status="pending",
            created_at=_now(),
        ),
    ])
    db_session.commit()

    response = client.get("/progress/dashboard", headers=headers_a)
    assert response.status_code == 200

    data = response.json()

    # summary
    summary = data["summary"]
    assert summary["total_sessions"] == 3
    assert summary["completed_sessions"] == 2
    assert summary["pending_sessions"] == 1
    assert summary["total_minutes"] == 180
    assert summary["total_hours"] == 3.0
    assert summary["progress_percentage"] == round(2 / 3 * 100, 2)

    # subjects
    assert len(data["subjects"]) == 1
    subject = data["subjects"][0]
    assert subject["subject_name"] == "Matemática"
    assert subject["completed_sessions"] == 2
    assert subject["pending_sessions"] == 1
    assert subject["total_minutes"] == 180

    # daily_progress — só completed, pending (20/08) não aparece
    daily = {item["date"]: item for item in data["daily_progress"]}
    assert len(daily) == 2
    assert daily["2026-08-18"]["minutes_studied"] == 60
    assert daily["2026-08-18"]["sessions_completed"] == 1
    assert daily["2026-08-19"]["minutes_studied"] == 120
    assert daily["2026-08-19"]["sessions_completed"] == 1
    assert "2026-08-20" not in daily


def test_dashboard_isolation(
    client, db_session, user_a, user_b, subject_1, headers_a, headers_b
):
    """User B não vê dados do User A no dashboard."""
    plan = StudyPlan(
        user_id=user_a.id,
        title="Plan A",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 31),
        created_at=_now(),
    )
    db_session.add(plan)
    db_session.commit()
    db_session.refresh(plan)

    sps = StudyPlanSubject(
        study_plan_id=plan.id,
        subject_id=subject_1.id,
        weekly_hours=4,
        created_at=_now(),
    )
    db_session.add(sps)
    db_session.commit()
    db_session.refresh(sps)

    db_session.add(StudySession(
        study_plan_subject_id=sps.id,
        session_date=date(2026, 8, 18),
        duration_minutes=90,
        status="completed",
        created_at=_now(),
    ))
    db_session.commit()

    # User B deve ver tudo zerado
    response_b = client.get("/progress/dashboard", headers=headers_b)
    assert response_b.status_code == 200

    data_b = response_b.json()
    assert data_b["summary"]["total_sessions"] == 0
    assert data_b["subjects"] == []
    assert data_b["daily_progress"] == []

    # User A vê seus próprios dados
    response_a = client.get("/progress/dashboard", headers=headers_a)
    data_a = response_a.json()
    assert data_a["summary"]["total_sessions"] == 1
    assert data_a["summary"]["completed_sessions"] == 1
