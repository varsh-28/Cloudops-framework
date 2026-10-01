import socket
import subprocess
import sys
import time

import pytest
from fastapi.testclient import TestClient
from playwright.sync_api import expect

from app.main import app


BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# SERVER MANAGEMENT
# ============================================================

def is_server_running(host="127.0.0.1", port=8000):
    """
    Check whether something is already listening on port 8000.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        return result == 0

    finally:
        sock.close()


@pytest.fixture(scope="session", autouse=True)
def start_application_server():
    """
    Start FastAPI automatically when pytest starts.

    This fixes Playwright's:
        ERR_CONNECTION_REFUSED

    It also works when GitHub Actions starts pytest directly.
    """

    process = None

    # If CI/workflow already started the server,
    # don't start another one.
    if not is_server_running():

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

        # Wait for FastAPI to become available.
        for _ in range(30):

            if is_server_running():
                break

            # Check whether uvicorn crashed.
            if process.poll() is not None:

                output = ""

                if process.stdout:
                    output = process.stdout.read()

                pytest.fail(
                    "FastAPI server failed to start.\n\n"
                    f"{output}"
                )

            time.sleep(1)

        else:

            process.terminate()

            pytest.fail(
                "FastAPI server did not start within 30 seconds."
            )

    try:

        yield

    finally:

        # Only terminate the server that this fixture started.
        if process is not None:

            process.terminate()

            try:
                process.wait(timeout=5)

            except subprocess.TimeoutExpired:

                process.kill()


# ============================================================
# API CLIENT
# ============================================================

@pytest.fixture
def api_client():
    """
    FastAPI TestClient used by API tests.
    """

    with TestClient(app) as client:

        yield client


@pytest.fixture
def client(api_client):
    """
    Backward-compatible alias.

    Some tests use:
        client

    Other tests use:
        api_client

    Both now point to the same FastAPI TestClient.
    """

    return api_client


# ============================================================
# AUTHENTICATION
# ============================================================

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

    data = response.json()

    return data["token"]


@pytest.fixture
def auth_headers(auth_token):

    return {
        "Authorization": f"Bearer {auth_token}"
    }


# ============================================================
# PLAYWRIGHT
# ============================================================

@pytest.fixture
def logged_in_page(page):

    page.goto("/")

    page.locator("#username").fill("admin")

    page.locator("#password").fill("admin123")

    page.get_by_role(
        "button",
        name="Login",
    ).click()

    expect(
        page.locator("#login-success-message")
    ).to_contain_text(
        "Login successful. Welcome admin."
    )

    return page