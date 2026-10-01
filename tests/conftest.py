import socket
import subprocess
import sys
import time

import pytest
from fastapi.testclient import TestClient
from playwright.sync_api import expect

from app.main import app
from utils.api_client import APIClient


BASE_URL = "http://127.0.0.1:8000"


def is_server_running(host="127.0.0.1", port=8000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0
    finally:
        sock.close()


@pytest.fixture(scope="session", autouse=True)
def start_application_server():
    process = None

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

        for _ in range(30):

            if is_server_running():
                break

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

        if process is not None:

            process.terminate()

            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


@pytest.fixture
def api_client():
    """
    Reusable APIClient wrapper.
    """

    with TestClient(app) as client:
        yield APIClient(client)


@pytest.fixture
def client(api_client):
    """
    Backward-compatible fixture.

    Existing tests using `client` continue to work.
    """

    return api_client


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

    return response.json()["token"]


@pytest.fixture
def auth_headers(auth_token):

    return {
        "Authorization": f"Bearer {auth_token}"
    }


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