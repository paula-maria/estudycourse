def test_user_cannot_access_another_users_goal(
    client,
    user,
    other_user,
    auth_headers,
    other_auth_headers,
):
    response = client.post(
        "/study-goals",
        json={
            "title": "Meta do usuário A",
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

    assert response.status_code == 201

    goal_id = response.json()["id"]

    response = client.get(
        f"/study-goals/{goal_id}",
        headers=other_auth_headers,
    )

    assert response.status_code == 404


def test_study_plan_ownership_security(client, auth_headers, other_auth_headers):
    # User A cria um plano de estudo
    plan_payload = {
        "title": "Plano do Usuario A",
        "start_date": "2026-09-01",
        "end_date": "2026-09-30",
    }
    plan_res = client.post("/study-plans", json=plan_payload, headers=auth_headers)
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

    response = client.post("/study-goals", json=goal_payload, headers=other_auth_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have access to this study plan"


def test_user_isolation_goals(client, auth_headers, other_auth_headers):
    # User A cria meta A
    payload_a = {
        "title": "Meta do Usuario A",
        "goal_type": "time",
        "target_value": 30,
        "start_date": "2026-09-01",
    }
    res_a = client.post("/study-goals", json=payload_a, headers=auth_headers)
    assert res_a.status_code == 201

    # User B cria meta B
    payload_b = {
        "title": "Meta do Usuario B",
        "goal_type": "content",
        "target_value": 40,
        "start_date": "2026-09-01",
    }
    res_b = client.post("/study-goals", json=payload_b, headers=other_auth_headers)
    assert res_b.status_code == 201

    # User A lista metas - não deve ver meta B
    list_a = client.get("/study-goals", headers=auth_headers)
    assert list_a.status_code == 200
    titles_a = [g["title"] for g in list_a.json()]
    assert "Meta do Usuario A" in titles_a
    assert "Meta do Usuario B" not in titles_a

    # User B lista metas - não deve ver meta A
    list_b = client.get("/study-goals", headers=other_auth_headers)
    assert list_b.status_code == 200
    titles_b = [g["title"] for g in list_b.json()]
    assert "Meta do Usuario B" in titles_b
    assert "Meta do Usuario A" not in titles_b
