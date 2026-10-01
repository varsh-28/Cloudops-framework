import pytest


@pytest.fixture
def authenticated_client(client):
    """
    Return an API client authenticated as the admin user.
    """
    client.login(
        username="admin",
        password="admin123",
    )
    return client


def test_deploy_service(authenticated_client):
    """
    Verify successful deployment of an existing service.
    """

    response = authenticated_client.deploy(
        service_name="payment-service",
        version="2.0.0",
    )

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert "deployment" in data

    deployment = data["deployment"]

    assert deployment["service_name"] == "payment-service"
    assert deployment["version"] == "2.0.0"
    assert deployment["status"] == "successful"
    assert deployment["environment"] == "qa"
    assert deployment["deployed_by"] == "admin"


def test_deploy_unknown_service(authenticated_client):
    """
    Verify deployment fails for an unknown service.
    """

    response = authenticated_client.deploy(
        service_name="unknown-service",
        version="2.0.0",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_deployment_history(authenticated_client):
    """
    Verify authenticated users can retrieve deployment history.
    """

    response = authenticated_client.get_deployment_history()

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "deployments" in data
    assert isinstance(data["deployments"], list)