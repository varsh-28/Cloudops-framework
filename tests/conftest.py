import pytest
from fastapi.testclient import TestClient

from app.main import app
from config.settings import BASE_URL
from utils.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    return TestClient(app)


@pytest.fixture
def client(api_client):
    return APIClient(api_client)


@pytest.fixture
def auth_token(api_client):
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
    return {
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session", autouse=True)
def start_application_server():
    """
    Start FastAPI for Playwright UI tests.
    """

    import subprocess
    import sys
    import time

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    time.sleep(2)

    yield

    process.terminate()

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()