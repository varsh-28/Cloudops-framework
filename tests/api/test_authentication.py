import pytest


LOGIN_CASES = [
    {
        "name": "valid_admin",
        "username": "admin",
        "password": "admin123",
        "expected_status": 200,
    },
    {
        "name": "invalid_password",
        "username": "admin",
        "password": "wrongpassword",
        "expected_status": 401,
    },
    {
        "name": "invalid_username",
        "username": "unknown",
        "password": "admin123",
        "expected_status": 401,
    },
    {
        "name": "empty_username",
        "username": "",
        "password": "admin123",
        "expected_status": 401,
    },
    {
        "name": "empty_password",
        "username": "admin",
        "password": "",
        "expected_status": 401,
    },
]


@pytest.mark.parametrize(
    "test_case",
    LOGIN_CASES,
    ids=[case["name"] for case in LOGIN_CASES],
)
def test_login_scenarios(api_client, test_case):

    response = api_client.post(
        "/api/login",
        json={
            "username": test_case["username"],
            "password": test_case["password"],
        },
    )

    assert response.status_code == test_case["expected_status"]


def test_successful_login_returns_token(api_client):

    response = api_client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert data["token"]


def test_invalid_login_does_not_return_token(api_client):

    response = api_client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert "token" not in data