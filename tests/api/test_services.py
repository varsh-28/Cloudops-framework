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
        "action": "restart",
        "expected_status": 200,
    },
]


@pytest.mark.parametrize(
    "test_case",
    SERVICE_ACTION_CASES,
    ids=[case["name"] for case in SERVICE_ACTION_CASES],
)
def test_service_actions(api_client, auth_headers, test_case):
    """
    Verify supported service actions.

    API endpoint:
        POST /api/services/{service_name}/action

    Request body:
        {"action": "start|stop|restart"}
    """

    response = api_client.post(
        "/api/services/payment-service/action",
        headers=auth_headers,
        json={
            "action": test_case["action"],
        },
    )

    assert response.status_code == test_case["expected_status"]

    data = response.json()

    assert "message" in data
    assert "service" in data

    assert data["service"]["name"] == "payment-service"


def test_health_check(api_client):
    """
    Verify the application health endpoint.

    API endpoint:
        GET /health
    """

    response = api_client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "cloudops-service"


def test_get_all_services(api_client, auth_headers):
    """
    Verify that all available services can be retrieved.

    API endpoint:
        GET /api/services
    """

    response = api_client.get(
        "/api/services",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "services" in data

    assert data["count"] == 3
    assert len(data["services"]) == 3


def test_get_existing_service(api_client, auth_headers):
    """
    Verify retrieval of an existing service.

    API endpoint:
        GET /api/services/{service_name}
    """

    response = api_client.get(
        "/api/services/payment-service",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "name" in data
    assert data["name"] == "payment-service"


def test_get_non_existing_service(api_client, auth_headers):
    """
    Verify that requesting an unknown service returns 404.
    """

    response = api_client.get(
        "/api/services/unknown-service",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_service_requires_authentication(api_client):
    """
    Verify that protected service endpoints require authentication.
    """

    response = api_client.get(
        "/api/services",
    )

    assert response.status_code == 401


def test_stop_service(api_client, auth_headers):
    """
    Verify that a service can be stopped.
    """

    response = api_client.post(
        "/api/services/payment-service/action",
        headers=auth_headers,
        json={
            "action": "stop",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["name"] == "payment-service"
    assert data["service"]["status"] == "stopped"


def test_start_service(api_client, auth_headers):
    """
    Verify that a service can be started.
    """

    response = api_client.post(
        "/api/services/payment-service/action",
        headers=auth_headers,
        json={
            "action": "start",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["name"] == "payment-service"
    assert data["service"]["status"] == "running"


def test_invalid_service_action(api_client, auth_headers):
    """
    Verify that an unsupported service action is rejected.
    """

    response = api_client.post(
        "/api/services/payment-service/action",
        headers=auth_headers,
        json={
            "action": "invalid-action",
        },
    )

    assert response.status_code == 400


def test_deploy_service(api_client, auth_headers):
    """
    Verify deployment of an existing service.

    API endpoint:
        POST /api/deploy
    """

    response = api_client.post(
        "/api/deploy",
        headers=auth_headers,
        json={
            "service_name": "payment-service",
            "version": "2.0.0",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert "deployment" in data

    assert data["deployment"]["service_name"] == "payment-service"
    assert data["deployment"]["version"] == "2.0.0"


def test_deploy_non_existing_service(api_client, auth_headers):
    """
    Verify deployment of an unknown service returns 404.
    """

    response = api_client.post(
        "/api/deploy",
        headers=auth_headers,
        json={
            "service_name": "unknown-service",
            "version": "1.0.0",
        },
    )

    assert response.status_code == 404


def test_deployment_history(api_client, auth_headers):
    """
    Verify deployment history.

    API endpoint:
        GET /api/deployments
    """

    # Create a deployment first.
    deploy_response = api_client.post(
        "/api/deploy",
        headers=auth_headers,
        json={
            "service_name": "user-service",
            "version": "2.0.0",
        },
    )

    assert deploy_response.status_code == 200

    # Retrieve deployment history.
    response = api_client.get(
        "/api/deployments",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "deployments" in data

    assert data["count"] >= 1
    assert len(data["deployments"]) >= 1

    latest = data["deployments"][-1]

    assert latest["service_name"] == "user-service"
    assert latest["version"] == "2.0.0"
    assert latest["status"] == "successful"