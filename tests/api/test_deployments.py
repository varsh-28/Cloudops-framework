import pytest


@pytest.fixture
def authenticated_client(client):
    """
    Return an APIClient that is authenticated as the admin user.
    """

    client.login(
        username="admin",
        password="admin123",
    )

    return client


def test_deploy_service(authenticated_client):
    response = authenticated_client.deploy(
        service_name="payment-service",
        version="2.0.0",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Deployment of payment-service version 2.0.0 successful"
    )

    assert "deployment" in data

    deployment = data["deployment"]

    assert deployment["service_name"] == "payment-service"
    assert deployment["version"] == "2.0.0"
    assert deployment["environment"] == "qa"
    assert deployment["status"] == "successful"
    assert deployment["deployed_by"] == "admin"

    assert "deployment_id" in deployment
    assert "timestamp" in deployment


def test_deploy_unknown_service(authenticated_client):
    response = authenticated_client.deploy(
        service_name="unknown-service",
        version="2.0.0",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Service not found"


def test_deployment_history(authenticated_client):
    response = authenticated_client.get_deployment_history()

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "deployments" in data

    assert isinstance(data["deployments"], list)

    assert data["count"] == len(data["deployments"])


def test_get_deployments_endpoint(api_client, auth_headers):
    response = api_client.get(
        "/api/deployments",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "deployments" in data

    assert isinstance(data["deployments"], list)

    assert data["count"] == len(data["deployments"])