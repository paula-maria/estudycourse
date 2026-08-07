def test_register_user(client):
    payload = {
        "name": "New User",
        "email": "newuser@test.com",
        "password": "strongpassword"
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == "newuser@test.com"

def test_register_duplicate_email(client, user_a):
    payload = {
        "name": "Another User",
        "email": "usera@test.com", # Same as user_a
        "password": "password"
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 400

def test_login_success(client, user_a):
    payload = {
        "email": "usera@test.com",
        "password": "senha123"
    }
    response = client.post("/users/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(client, user_a):
    payload = {
        "email": "usera@test.com",
        "password": "wrongpassword"
    }
    response = client.post("/users/login", json=payload)
    assert response.status_code == 401

def test_get_me_success(client, headers_a):
    response = client.get("/users/me", headers=headers_a)
    assert response.status_code == 200
    assert response.json()["email"] == "usera@test.com"

def test_get_me_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401
