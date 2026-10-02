import pytest

from app.main import ACTIVE_TOKENS


LOGIN_URL = "/api/login"

VALID_CREDENTIALS = {
    "username": "admin",
    "password": "admin123",
}


@pytest.mark.parametrize(
    "test_case",
    [
        {
            "name": "valid_admin",
            "payload": {
                "username": "admin",
                "password": "admin123",
            },
            "expected_status": 200,
        },
        {
            "name": "invalid_password",
            "payload": {
                "username": "admin",
                "password": "wrong-password",
            },
            "expected_status": 401,
        },
        {
            "name": "invalid_username",
            "payload": {
                "username": "unknown-user",
                "password": "admin123",
            },
            "expected_status": 401,
        },
        {
            "name": "empty_username",
            "payload": {
                "username": "",
                "password": "admin123",
            },
            "expected_status": 401,
        },
        {
            "name": "empty_password",
            "payload": {
                "username": "admin",
                "password": "",
            },
            "expected_status": 401,
        },
    ],
    ids=lambda case: case["name"],
)
def test_login_scenarios(api_client, test_case):
    response = api_client.post(
        LOGIN_URL,
        json=test_case["payload"],
    )

    assert response.status_code == test_case["expected_status"]

    data = response.json()

    if test_case["expected_status"] == 200:
        assert data["message"] == "Login successful"
        assert "token" in data
        assert "access_token" in data
        assert data["username"] == "admin"
        assert data["role"] == "admin"

    else:
        assert data["detail"] == "Invalid username or password"


def test_successful_login_returns_token(api_client):
    response = api_client.post(
        LOGIN_URL,
        json=VALID_CREDENTIALS,
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert "access_token" in data
    assert data["token"] == data["access_token"]
    assert data["username"] == "admin"
    assert data["role"] == "admin"

    token = data["access_token"]

    assert token in ACTIVE_TOKENS
    assert ACTIVE_TOKENS[token] == "admin"


def test_invalid_login_does_not_return_token(api_client):
    response = api_client.post(
        LOGIN_URL,
        json={
            "username": "admin",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid username or password"
    assert "token" not in data
    assert "access_token" not in data


def test_missing_authentication_header(api_client):
    response = api_client.get("/api/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_invalid_authentication_scheme(api_client):
    response = api_client.get(
        "/api/me",
        headers={
            "Authorization": "Basic invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication scheme"


def test_invalid_authentication_token(api_client):
    response = api_client.get(
        "/api/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Invalid or expired authentication token"
    )


def test_empty_bearer_token(api_client):
    response = api_client.get(
        "/api/me",
        headers={
            "Authorization": "Bearer ",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Invalid or expired authentication token"
    )


def test_current_user(api_client, auth_headers):
    response = api_client.get(
        "/api/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "admin"
    assert data["role"] == "admin"


def test_authenticated_token_for_deleted_user(api_client):
    token = "test-token-deleted-user"

    ACTIVE_TOKENS[token] = "deleted-user"

    try:
        response = api_client.get(
            "/api/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "User not found"

    finally:
        ACTIVE_TOKENS.pop(token, None)