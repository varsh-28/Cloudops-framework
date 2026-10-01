import pytest
from fastapi.testclient import TestClient

from app.main import app
from config.settings import BASE_URL


@pytest.fixture(scope="session")
def api_client():
    """
    Shared FastAPI test client.

    The application is tested in-process, so BASE_URL is retained
    as the framework's environment configuration while TestClient
    handles the actual API requests.
    """
    return TestClient(app)


@pytest.fixture
def auth_token(api_client):
    """Return a valid authentication token for API tests."""

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
    """Return authorization headers for authenticated requests."""

    return {
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture(scope="session")
def base_url():
    """Return the configured application base URL."""

    return BASE_URL
