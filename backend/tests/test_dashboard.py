from datetime import date

from app.study_plan_subjects.model import StudyPlanSubject
from app.study_plans.model import StudyPlan
from app.study_sessions.model import StudySession


def test_get_dashboard(
    client, db_session, user_a, subject_1, headers_a
):
    """O Dashboard deve retornar o sumário, progresso por matérias e evolução diária."""
    
    # Criar plano e matéria
    plan = StudyPlan(
        user_id=user_a.id,
        title="Dashboard Plan",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 31),
        created_at=date(2026, 1, 1),
    )
    db_session.add(plan)
    db_session.commit()
    db_session.refresh(plan)

    sps = StudyPlanSubject(
        study_plan_id=plan.id,
        subject_id=subject_1.id,
        weekly_hours=4,
        created_at=date(2026, 1, 1),
    )
    db_session.add(sps)
    db_session.commit()
    db_session.refresh(sps)

    # Adicionar sessões (2 completadas, 1 pendente)
    session1 = StudySession(
        study_plan_subject_id=sps.id,
        session_date=date(2026, 8, 18),
        duration_minutes=60,
        status="completed",
        created_at=date(2026, 1, 1),
    )
    session2 = StudySession(
        study_plan_subject_id=sps.id,
        session_date=date(2026, 8, 19),
        duration_minutes=120,
        status="completed",
        created_at=date(2026, 1, 1),
    )
    session3 = StudySession(
        study_plan_subject_id=sps.id,
        session_date=date(2026, 8, 20),
        duration_minutes=45,
        status="pending",
        created_at=date(2026, 1, 1),
    )
    db_session.add_all([session1, session2, session3])
    db_session.commit()

    response = client.get("/dashboard", headers=headers_a)

    assert response.status_code == 200

    data = response.json()
    
    # Verificar chaves principais
    assert "summary" in data
    assert "subjects" in data
    assert "daily_progress" in data

    # Validar Summary
    summary = data["summary"]
    assert summary["total_sessions"] == 3
    assert summary["completed_sessions"] == 2
    assert summary["pending_sessions"] == 1
    assert summary["total_minutes"] == 180
    assert summary["progress_percentage"] == round((2 / 3) * 100, 2)

    # Validar Subjects
    assert len(data["subjects"]) == 1
    subject_progress = data["subjects"][0]
    assert subject_progress["subject_name"] == "Matemática"
    assert subject_progress["completed_sessions"] == 2

    # Validar Daily Progress
    daily = data["daily_progress"]
    assert len(daily) == 2
    assert daily[0]["date"] == "2026-08-18"
    assert daily[0]["minutes_studied"] == 60
    assert daily[1]["date"] == "2026-08-19"
    assert daily[1]["minutes_studied"] == 120
