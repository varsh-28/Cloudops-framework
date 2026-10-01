import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def api_client():
    """
    Creates a fresh FastAPI TestClient for each test.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client(api_client):
    """
    Backward-compatible alias for tests that use `client`.
    """
    return api_client


@pytest.fixture
def auth_token(api_client):
    """
    Logs in as admin and returns the authentication token.

    Supports both:
    - access_token
    - token
    """

    response = api_client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200, (
        "Login failed.\n"
        f"Status: {response.status_code}\n"
        f"Response: {response.text}"
    )

    data = response.json()

    token = data.get("access_token") or data.get("token")

    assert token, (
        "Login succeeded but no authentication token was returned.\n"
        f"Response JSON: {data}"
    )

    return token


@pytest.fixture
def auth_headers(auth_token):
    """
    Creates the Authorization header required
    by protected API endpoints.
    """
    return {
        "Authorization": f"Bearer {auth_token}"
    }
