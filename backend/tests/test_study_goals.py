def test_create_study_goal(client, headers_a):
    payload = {
        "title": "Passar no Concurso",
        "description": "Meta principal de 2026",
        "goal_type": "time",
        "target_value": 100,
        "start_date": "2026-09-01",
        "end_date": "2026-12-31",
        "is_primary": True,
    }

    response = client.post("/study-goals", json=payload, headers=headers_a)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Passar no Concurso"
    assert data["target_value"] == 100
    assert data["current_value"] == 0
    assert data["progress_percentage"] == 0.0
    assert data["is_primary"] is True


def test_study_goal_progress_percentage(client, headers_a, db_session):
    from app.study_goals.model import StudyGoal

    payload = {
        "title": "Ler 50 páginas",
        "goal_type": "content",
        "target_value": 200,
        "start_date": "2026-09-01",
    }

    response = client.post("/study-goals", json=payload, headers=headers_a)
    assert response.status_code == 201
    goal_id = response.json()["id"]

    # Simular atualização do current_value
    db_goal = db_session.query(StudyGoal).filter(StudyGoal.id == goal_id).first()
    db_goal.current_value = 50
    db_session.commit()

    get_response = client.get(f"/study-goals/{goal_id}", headers=headers_a)
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["current_value"] == 50
    assert data["progress_percentage"] == 25.0


def test_study_plan_ownership_security(client, headers_a, headers_b):
    # User A cria um plano de estudo
    plan_payload = {
        "title": "Plano do Usuario A",
        "start_date": "2026-09-01",
        "end_date": "2026-09-30",
    }
    plan_res = client.post("/study-plans", json=plan_payload, headers=headers_a)
    assert plan_res.status_code == 201
    user_a_plan_id = plan_res.json()["id"]

    # User B tenta vincular a meta ao plano do User A
    goal_payload = {
        "title": "Meta do Usuario B",
        "study_plan_id": user_a_plan_id,
        "goal_type": "time",
        "target_value": 50,
        "start_date": "2026-09-01",
    }

    response = client.post("/study-goals", json=goal_payload, headers=headers_b)
    assert response.status_code == 404
    assert response.json()["detail"] == "Study plan not found"
