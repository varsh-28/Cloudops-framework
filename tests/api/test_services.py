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


@pytest.mark.parametrize(
    "test_case",
    SERVICE_ACTION_CASES,
    ids=[case["name"] for case in SERVICE_ACTION_CASES],
)
def test_service_actions(api_client, auth_token, test_case):
    response = api_client.post(
        f"/api/services/payment-service/{test_case['action']}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == test_case["expected_status"]


def test_health_check(api_client):
    response = api_client.get("/api/services/health")

    assert response.status_code == 200


def test_get_all_services(api_client, auth_token):
    response = api_client.get(
        "/api/services",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200


def test_get_existing_service(api_client, auth_token):
    response = api_client.get(
        "/api/services/payment-service",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200


def test_get_non_existing_service(api_client, auth_token):
    response = api_client.get(
        "/api/services/unknown-service",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 404


def test_service_requires_authentication(api_client):
    response = api_client.get("/api/services")

    assert response.status_code in (401, 403)


def test_invalid_service_action(api_client, auth_token):
    response = api_client.post(
        "/api/services/payment-service/restart",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code in (400, 404, 405)


def test_deploy_non_existing_service(api_client, auth_token):
    response = api_client.post(
        "/api/services/unknown-service/deploy",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 404


def test_deployment_history(api_client, auth_token):
    response = api_client.get(
        "/api/deployments/history",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200