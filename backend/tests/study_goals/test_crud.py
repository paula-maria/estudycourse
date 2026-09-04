from datetime import date

from app.study_goals.model import StudyGoal


def test_create_study_goal(client, auth_headers):
    response = client.post(
        "/study-goals",
        json={
            "title": "Zerar edital",
            "description": "Concluir todo o conteúdo",
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": 100,
            "start_date": "2026-09-04",
            "end_date": "2026-12-20",
            "is_primary": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Zerar edital"
    assert data["goal_type"] == "content"
    assert data["target_value"] == 100
    assert data["current_value"] == 0
    assert data["progress_percentage"] == 0
    assert data["status"] == "active"
    assert data["is_primary"] is True


def test_list_study_goals(client, auth_headers):
    client.post(
        "/study-goals",
        json={
            "title": "Estudar matemática",
            "description": None,
            "study_plan_id": None,
            "goal_type": "time",
            "target_value": 600,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    response = client.get(
        "/study-goals",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Estudar matemática"


def test_get_study_goal(client, auth_headers):
    create_response = client.post(
        "/study-goals",
        json={
            "title": "Resolver questões",
            "description": "Resolver questões diariamente",
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": 500,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = create_response.json()["id"]

    response = client.get(
        f"/study-goals/{goal_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == goal_id
    assert data["title"] == "Resolver questões"


def test_update_study_goal(client, auth_headers):
    create_response = client.post(
        "/study-goals",
        json={
            "title": "Estudar português",
            "description": None,
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": 50,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = create_response.json()["id"]

    response = client.put(
        f"/study-goals/{goal_id}",
        json={
            "title": "Estudar português e redação",
            "target_value": 100,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Estudar português e redação"
    assert data["target_value"] == 100


def test_delete_study_goal(client, auth_headers):
    create_response = client.post(
        "/study-goals",
        json={
            "title": "Meta temporária",
            "description": None,
            "study_plan_id": None,
            "goal_type": "time",
            "target_value": 300,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = create_response.json()["id"]

    response = client.delete(
        f"/study-goals/{goal_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/study-goals/{goal_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_list_goals_requires_authentication(client):
    response = client.get("/study-goals")

    assert response.status_code == 401


def test_create_goal_requires_authentication(client):
    response = client.post(
        "/study-goals",
        json={
            "title": "Meta",
            "description": None,
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": 10,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
    )

    assert response.status_code == 401


def test_goal_requires_positive_target(client, auth_headers):
    response = client.post(
        "/study-goals",
        json={
            "title": "Meta inválida",
            "description": None,
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": 0,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_goal_rejects_negative_target(client, auth_headers):
    response = client.post(
        "/study-goals",
        json={
            "title": "Meta inválida",
            "description": None,
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": -10,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_goal_rejects_invalid_dates(client, auth_headers):
    response = client.post(
        "/study-goals",
        json={
            "title": "Meta inválida",
            "description": None,
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": 100,
            "start_date": "2026-12-20",
            "end_date": "2026-09-04",
            "is_primary": False,
        },
        headers=auth_headers,
    )

    assert response.status_code == 400
