def test_health_check(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "cloudops-service"


def test_get_all_services(api_client, auth_headers):
    response = api_client.get(
        "/api/services",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert len(data["services"]) == 3


def test_get_existing_service(api_client, auth_headers):
    response = api_client.get(
        "/api/services/payment-service",
        headers=auth_headers,
    )

    assert response.status_code == 200

    service = response.json()

    assert service["name"] == "payment-service"
    assert service["environment"] == "qa"
    assert service["status"] == "running"


def test_get_non_existing_service(api_client, auth_headers):
    response = api_client.get(
        "/api/services/does-not-exist",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_service_requires_authentication(api_client):
    response = api_client.get(
        "/api/services"
    )

    assert response.status_code == 401


def test_stop_service(api_client, auth_headers):
    response = api_client.post(
        "/api/services/payment-service/action",
        headers=auth_headers,
        json={
            "action": "stop"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["status"] == "stopped"


def test_start_service(api_client, auth_headers):
    response = api_client.post(
        "/api/services/payment-service/action",
        headers=auth_headers,
        json={
            "action": "start"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"]["status"] == "running"


def test_invalid_service_action(api_client, auth_headers):
    response = api_client.post(
        "/api/services/payment-service/action",
        headers=auth_headers,
        json={
            "action": "destroy"
        },
    )

    assert response.status_code == 400


def test_deploy_service(api_client, auth_headers):
    response = api_client.post(
        "/api/deploy",
        headers=auth_headers,
        json={
            "service_name": "payment-service",
            "version": "2.5.0",
        },
    )

    assert response.status_code == 200

    deployment = response.json()

    assert deployment["service_name"] == "payment-service"
    assert deployment["version"] == "2.5.0"
    assert deployment["environment"] == "qa"
    assert deployment["status"] == "successful"
    assert deployment["deployed_by"] == "admin"


def test_deploy_non_existing_service(
    api_client,
    auth_headers,
):
    response = api_client.post(
        "/api/deploy",
        headers=auth_headers,
        json={
            "service_name": "unknown-service",
            "version": "1.0.0",
        },
    )

    assert response.status_code == 404


def test_deployment_history(
    api_client,
    auth_headers,
):
    # Create deployment
    deploy_response = api_client.post(
        "/api/deploy",
        headers=auth_headers,
        json={
            "service_name": "user-service",
            "version": "2.0.0",
        },
    )

    assert deploy_response.status_code == 200

    # Check history
    response = api_client.get(
        "/api/deployments",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] >= 1

    latest = data["deployments"][-1]

    assert latest["service_name"] == "user-service"
    assert latest["version"] == "2.0.0"
    assert latest["status"] == "successful"