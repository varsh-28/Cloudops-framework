import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def api_client():
    """
    Creates a fresh API client for each test.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client(api_client):
    """
    Backward-compatible alias for the API client.

    Some API tests use the fixture name `client`,
    while newer tests use `api_client`.
    """
    return api_client


@pytest.fixture
def auth_token(api_client):
    """
    Logs in as admin and returns the authentication token.
    """
    response = api_client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """
    Returns authentication headers using the generated token.
    """
    return {
        "Authorization": f"Bearer {auth_token}",
    }
