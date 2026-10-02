import pytest


def test_application_info(api_client):
    """
    Verify the application information endpoint.
    """

    response = api_client.get("/api/info")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "CloudOps SDET Framework"
    assert data["version"] == "1.0.0"
    assert data["environment"] == "qa"
    assert data["service_count"] == 3
    assert "deployment_count" in data


def test_root_page(api_client):
    """
    Verify the root login page loads successfully.
    """

    response = api_client.get("/")

    assert response.status_code == 200
    assert "CloudOps Login" in response.text
    assert "login-form" in response.text
    assert "username" in response.text
    assert "password" in response.text


def test_dashboard_page(api_client):
    """
    Verify the dashboard endpoint renders all configured services.

    This test is intentionally performed through the FastAPI TestClient
    so pytest-cov records execution of the dashboard function.
    """

    response = api_client.get("/dashboard")

    assert response.status_code == 200

    html = response.text

    assert "CloudOps Dashboard" in html

    assert "payment-service" in html
    assert "user-service" in html
    assert "order-service" in html

    assert "running" in html
    assert "1.0.0" in html
    assert "qa" in html