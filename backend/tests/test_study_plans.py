def test_create_study_plan(client):
    payload = {
        "title": "Meu Plano de Estudos",
        "description": "Focar em backend",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    
    response = client.post("/study-plans", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Meu Plano de Estudos"
    assert data["description"] == "Focar em backend"
    assert "id" in data
    assert data["user_id"] == 1

def test_create_study_plan_invalid_dates(client):
    payload = {
        "title": "Plano Inválido",
        "start_date": "2026-08-31",
        "end_date": "2026-08-01"
    }
    
    response = client.post("/study-plans", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "End date must be after start date"

def test_list_study_plans(client):
    response = client.get("/study-plans")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == "Meu Plano de Estudos"

def test_get_study_plan(client):
    # First, let's get the list to find the ID
    response = client.get("/study-plans")
    plan_id = response.json()[0]["id"]
    
    # Then fetch by ID
    response = client.get(f"/study-plans/{plan_id}")
    assert response.status_code == 200
    assert response.json()["id"] == plan_id
