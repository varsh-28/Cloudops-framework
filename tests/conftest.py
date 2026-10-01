import subprocess
import sys
import time
import urllib.error
import urllib.request

import pytest
from fastapi.testclient import TestClient

from app.main import app


BASE_URL = "http://127.0.0.1:8000"
HEALTH_URL = f"{BASE_URL}/health"


def is_server_running():
    """
    Checks whether the FastAPI application is already running.
    """
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return False


def wait_for_server(timeout=15):
    """
    Waits until the FastAPI server becomes available.
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        if is_server_running():
            return True

        time.sleep(0.5)

    return False


@pytest.fixture(scope="session", autouse=True)
def application_server():
    """
    Automatically starts the FastAPI application for the test session.

    If a server is already running on port 8000, it reuses it.

    This allows UI tests to run with:

        pytest -v

    without manually starting Uvicorn.
    """

    # ---------------------------------------------------------
    # Check whether the application is already running
    # ---------------------------------------------------------
    if is_server_running():
        print("\n[SERVER] Existing FastAPI server detected.")
        print(f"[SERVER] Using {BASE_URL}")

        yield

        return

    # ---------------------------------------------------------
    # Start FastAPI application
    # ---------------------------------------------------------
    print("\n[SERVER] Starting FastAPI application...")

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
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # ---------------------------------------------------------
    # Wait for application to become ready
    # ---------------------------------------------------------
    if not wait_for_server(timeout=15):
        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

        output, _ = process.communicate()

        raise RuntimeError(
            "FastAPI application failed to start.\n\n"
            f"Server output:\n{output}"
        )

    print(f"[SERVER] FastAPI application started at {BASE_URL}")

    # ---------------------------------------------------------
    # Run tests
    # ---------------------------------------------------------
    yield

    # ---------------------------------------------------------
    # Shutdown application
    # ---------------------------------------------------------
    print("\n[SERVER] Stopping FastAPI application...")

    process.terminate()

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()

    print("[SERVER] FastAPI application stopped.")


@pytest.fixture
def api_client():
    """
    Creates a fresh FastAPI TestClient for each API test.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client(api_client):
    """
    Backward-compatible alias.

    Some API tests use `client`,
    while others use `api_client`.
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