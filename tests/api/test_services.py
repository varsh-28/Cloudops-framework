import pytest


SERVICE_NAME = "payment-service"


SERVICE_ACTION_CASES = [
    {
        "name": "stop_service",
        "action": "stop",
        "expected_status": 200,
        "service_status": "stopped",
    },
    {
        "name": "start_service",
        "action": "start",
        "expected_status": 200,
        "service_status": "running",
    },
    {
        "name": "deploy_service",
        "action": "deploy",
        "expected_status": 200,
        "service_status": "running",
    },
    {
        "name": "restart_service",
        "action": "restart",
        "expected_status": 200,
        "service_status": "running",
    },
]


@pytest.mark.parametrize(
    "test_case",
    SERVICE_ACTION_CASES,
    ids=[case["name"] for case in SERVICE_ACTION_CASES],
)
def test_service_actions(api_client, auth_headers, test_case):
    """
    Verify all supported service actions.
    """

    response = api_client.post(
        f"/api/services/{SERVICE_NAME}/action",
        headers=auth_headers,
        json={
            "action": test_case["action"],
        },
    )

    assert response.status_code == test_case["expected_status"]

    data = response.json()

    assert "message" in data
    assert "service" in data
    assert data["service"]["name"] == SERVICE_NAME
    assert data["service"]["status"] == test_case["service_status"]
    assert data["performed_by"] == "admin"


def test_health_check(api_client, auth_headers):
    """
    Verify the authenticated service health endpoint.
    """

    response = api_client.get(
        "/api/services/health",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "cloudops-service"
    assert data["services"] == 3


def test_get_all_services(api_client, auth_headers):
    """
    Verify retrieval of all services.
    """

    response = api_client.get(
        "/api/services",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert len(data["services"]) == 3

    service_names = {
        service["name"]
        for service in data["services"]
    }

    assert "payment-service" in service_names
    assert "user-service" in service_names
    assert "order-service" in service_names


def test_get_existing_service(api_client, auth_headers):
    """
    Verify retrieval of an existing service.
    """

    response = api_client.get(
        f"/api/services/{SERVICE_NAME}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == SERVICE_NAME
    assert "status" in data
    assert "version" in data
    assert data["environment"] == "qa"


def test_get_non_existing_service(api_client, auth_headers):
    """
    Verify that requesting an unknown service returns 404.
    """

    response = api_client.get(
        "/api/services/unknown-service",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_service_requires_authentication(api_client):
    """
    Verify that protected service endpoints require authentication.
    """

    response = api_client.get("/api/services")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_stop_service(api_client, auth_headers):
    """
    Verify that a service can be stopped.
    """

    response = api_client.post(
        f"/api/services/{SERVICE_NAME}/action",
        headers=auth_headers,
        json={
            "action": "stop",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["status"] == "stopped"


def test_start_service(api_client, auth_headers):
    """
    Verify that a stopped service can be started.
    """

    response = api_client.post(
        f"/api/services/{SERVICE_NAME}/action",
        headers=auth_headers,
        json={
            "action": "start",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["status"] == "running"


def test_invalid_service_action(api_client, auth_headers):
    """
    Verify that unsupported service actions are rejected.
    """

    response = api_client.post(
        f"/api/services/{SERVICE_NAME}/action",
        headers=auth_headers,
        json={
            "action": "invalid-action",
        },
    )

    assert response.status_code == 400

    detail = response.json()["detail"]

    assert "Invalid action" in detail
    assert "Allowed actions" in detail


def test_deploy_service(api_client, auth_headers):
    """
    Verify deployment through the service action endpoint.
    """

    response = api_client.post(
        f"/api/services/{SERVICE_NAME}/action",
        headers=auth_headers,
        json={
            "action": "deploy",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["name"] == SERVICE_NAME
    assert data["service"]["status"] == "running"


def test_deploy_non_existing_service(api_client, auth_headers):
    """
    Verify deployment action rejects unknown services.
    """

    response = api_client.post(
        "/api/services/unknown-service/action",
        headers=auth_headers,
        json={
            "action": "deploy",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_deployment_history(api_client, auth_headers):
    """
    Verify deployment history endpoint is accessible.
    """

    response = api_client.get(
        "/api/deployments/history",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "deployments" in data
    assert isinstance(data["count"], int)
    assert isinstance(data["deployments"], list)