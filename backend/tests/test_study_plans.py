def test_create_study_plan(client, headers_a):
    payload = {
        "title": "Meu Plano de Estudos",
        "description": "Focar em backend",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    
    response = client.post("/study-plans", json=payload, headers=headers_a)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Meu Plano de Estudos"
    assert data["description"] == "Focar em backend"
    assert "id" in data
    # Do not check exact user_id value because it might vary, but we know it should belong to user_a
    assert "user_id" in data

def test_create_study_plan_invalid_dates(client, headers_a):
    payload = {
        "title": "Plano Inválido",
        "start_date": "2026-08-31",
        "end_date": "2026-08-01"
    }
    
    response = client.post("/study-plans", json=payload, headers=headers_a)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "End date must be after start date"

def test_list_study_plans(client, headers_a):
    payload = {
        "title": "Meu Plano de Estudos",
        "description": "Focar em backend",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    client.post("/study-plans", json=payload, headers=headers_a)

    response = client.get("/study-plans", headers=headers_a)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == "Meu Plano de Estudos"

def test_get_study_plan(client, headers_a):
    payload = {
        "title": "Meu Plano de Estudos",
        "description": "Focar em backend",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    create_res = client.post("/study-plans", json=payload, headers=headers_a)
    plan_id = create_res.json()["id"]
    
    # Then fetch by ID
    response = client.get(f"/study-plans/{plan_id}", headers=headers_a)
    assert response.status_code == 200
    assert response.json()["id"] == plan_id

def test_isolation_study_plans(client, headers_a, headers_b):
    payload = {
        "title": "Meu Plano de Estudos",
        "description": "Focar em backend",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    create_res = client.post("/study-plans", json=payload, headers=headers_a)
    plan_id = create_res.json()["id"]

    # User B should NOT be able to get User A's plan
    response_b = client.get(f"/study-plans/{plan_id}", headers=headers_b)
    assert response_b.status_code in [403, 404]

    # User B should NOT be able to update User A's plan
    payload = {
        "title": "Plano Hacker",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    response_b_put = client.put(f"/study-plans/{plan_id}", json=payload, headers=headers_b)
    assert response_b_put.status_code in [403, 404]

    # User B should NOT be able to delete User A's plan
    response_b_delete = client.delete(f"/study-plans/{plan_id}", headers=headers_b)
    assert response_b_delete.status_code in [403, 404]
