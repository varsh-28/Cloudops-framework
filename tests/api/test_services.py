import pytest


SERVICE_ACTION_CASES = [
    {
        "name": "stop_service",
        "action": "stop",
        "expected_status": 200,
    },
    {
        "name": "start_service",
        "action": "start",
        "expected_status": 200,
    },
    {
        "name": "deploy_service",
        "action": "deploy",
        "expected_status": 200,
    },
]


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


@pytest.mark.parametrize(
    "test_case",
    SERVICE_ACTION_CASES,
    ids=[case["name"] for case in SERVICE_ACTION_CASES],
)
def test_service_actions(authenticated_client, test_case):
    """
    Verify supported service actions.
    """

    response = authenticated_client.service_action(
        service_name="payment-service",
        action=test_case["action"],
    )

    assert response.status_code == test_case["expected_status"]

    data = response.json()

    assert "message" in data
    assert "service" in data
    assert "performed_by" in data

    assert data["service"]["name"] == "payment-service"
    assert data["performed_by"] == "admin"


def test_health_check(client):
    """
    Verify the service health endpoint.
    """

    response = client.get_service_health()

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "cloudops-service"
    assert "services" in data


def test_get_all_services(authenticated_client):
    """
    Verify retrieval of all services.
    """

    response = authenticated_client.get_services()

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "services" in data
    assert data["count"] == 3
    assert len(data["services"]) == 3


def test_get_existing_service(authenticated_client):
    """
    Verify retrieval of an existing service.
    """

    response = authenticated_client.get_service(
        "payment-service"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "payment-service"
    assert data["status"] in ["running", "stopped"]
    assert "version" in data
    assert data["environment"] == "qa"


def test_get_non_existing_service(authenticated_client):
    """
    Verify requesting an unknown service returns 404.
    """

    response = authenticated_client.get_service(
        "unknown-service"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_service_requires_authentication(client):
    """
    Verify service APIs reject unauthenticated requests.
    """

    response = client.get("/api/services")

    assert response.status_code == 401


def test_stop_service(authenticated_client):
    """
    Verify a service can be stopped.
    """

    response = authenticated_client.service_action(
        service_name="payment-service",
        action="stop",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["name"] == "payment-service"
    assert data["service"]["status"] == "stopped"


def test_start_service(authenticated_client):
    """
    Verify a service can be started.
    """

    response = authenticated_client.service_action(
        service_name="payment-service",
        action="start",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["name"] == "payment-service"
    assert data["service"]["status"] == "running"


def test_invalid_service_action(authenticated_client):
    """
    Verify unsupported service actions return 400.
    """

    response = authenticated_client.service_action(
        service_name="payment-service",
        action="invalid-action",
    )

    assert response.status_code == 400

    data = response.json()

    assert "detail" in data
    assert "Invalid action" in data["detail"]


def test_deploy_service(authenticated_client):
    """
    Verify deployment through the service action endpoint.
    """

    response = authenticated_client.service_action(
        service_name="payment-service",
        action="deploy",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["name"] == "payment-service"
    assert data["service"]["status"] == "running"


def test_deploy_non_existing_service(authenticated_client):
    """
    Verify deployment of an unknown service fails.
    """

    response = authenticated_client.service_action(
        service_name="unknown-service",
        action="deploy",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_deployment_history(authenticated_client):
    """
    Verify deployment history can be retrieved.
    """

    response = authenticated_client.get_deployment_history()

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "deployments" in data
    assert isinstance(data["deployments"], list)