def test_goal_is_completed_when_target_is_reached(
    client,
    auth_headers,
):
    response = client.post(
        "/study-goals",
        json={
            "title": "Estudar Python",
            "description": None,
            "study_plan_id": None,
            "goal_type": "time",
            "target_value": 100,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = response.json()["id"]

    response = client.post(
        f"/study-goals/{goal_id}/progress?value=100",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_value"] == 100
    assert data["progress_percentage"] == 100
    assert data["status"] == "completed"


def test_goal_progress_cannot_exceed_target(
    client,
    auth_headers,
):
    response = client.post(
        "/study-goals",
        json={
            "title": "Resolver questões",
            "description": None,
            "study_plan_id": None,
            "goal_type": "questions",
            "target_value": 100,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = response.json()["id"]

    client.post(
        f"/study-goals/{goal_id}/progress?value=80",
        headers=auth_headers,
    )

    response = client.post(
        f"/study-goals/{goal_id}/progress?value=50",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_value"] == 100
    assert data["progress_percentage"] == 100
    assert data["status"] == "completed"


def test_goal_progress_cannot_be_negative(
    client,
    auth_headers,
):
    response = client.post(
        "/study-goals",
        json={
            "title": "Estudar matemática",
            "description": None,
            "study_plan_id": None,
            "goal_type": "time",
            "target_value": 100,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = response.json()["id"]

    response = client.post(
        f"/study-goals/{goal_id}/progress?value=-10",
        headers=auth_headers,
    )

    assert response.status_code == 400


def test_completed_goal_cannot_receive_more_progress(
    client,
    auth_headers,
):
    response = client.post(
        "/study-goals",
        json={
            "title": "Meta concluída",
            "description": None,
            "study_plan_id": None,
            "goal_type": "content",
            "target_value": 100,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = response.json()["id"]

    client.post(
        f"/study-goals/{goal_id}/progress?value=100",
        headers=auth_headers,
    )

    response = client.post(
        f"/study-goals/{goal_id}/progress?value=10",
        headers=auth_headers,
    )

    assert response.status_code == 400


def test_progress_zero_is_rejected(
    client,
    auth_headers,
):
    response = client.post(
        "/study-goals",
        json={
            "title": "Meta qualquer",
            "description": None,
            "study_plan_id": None,
            "goal_type": "time",
            "target_value": 100,
            "start_date": "2026-09-04",
            "end_date": None,
            "is_primary": False,
        },
        headers=auth_headers,
    )

    goal_id = response.json()["id"]

    response = client.post(
        f"/study-goals/{goal_id}/progress?value=0",
        headers=auth_headers,
    )

    assert response.status_code == 400


def test_progress_accumulates_correctly(
    client,
    auth_headers,
):
    response = client.post(
        "/study-goals",
        json={
            "title": "Acúmulo de progresso",
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

    goal_id = response.json()["id"]

    client.post(
        f"/study-goals/{goal_id}/progress?value=200",
        headers=auth_headers,
    )
    client.post(
        f"/study-goals/{goal_id}/progress?value=220",
        headers=auth_headers,
    )
    response = client.post(
        f"/study-goals/{goal_id}/progress?value=60",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["current_value"] == 480
    assert data["progress_percentage"] == 80.0
    assert data["status"] == "active"
