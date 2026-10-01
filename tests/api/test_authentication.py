def test_valid_login(client):
    response = client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["username"] == "admin"
    assert data["role"] == "admin"
    assert "token" in data


def test_invalid_password(client):
    response = client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_invalid_username(client):
    response = client.post(
        "/api/login",
        json={
            "username": "unknown-user",
            "password": "admin123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"