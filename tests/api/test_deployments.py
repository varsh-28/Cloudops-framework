def get_auth_token(client):
    response = client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    return response.json()["token"]


def test_deploy_service(client):
    token = get_auth_token(client)

    response = client.post(
        "/api/deploy",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_name": "payment-service",
            "version": "2.5.0",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service_name"] == "payment-service"
    assert data["version"] == "2.5.0"
    assert data["environment"] == "qa"
    assert data["status"] == "successful"
    assert data["deployed_by"] == "admin"


def test_deploy_unknown_service(client):
    token = get_auth_token(client)

    response = client.post(
        "/api/deploy",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_name": "unknown-service",
            "version": "1.0.0",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_deployment_history(client):
    token = get_auth_token(client)

    client.post(
        "/api/deploy",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_name": "user-service",
            "version": "2.0.0",
        },
    )

    response = client.get(
        "/api/deployments",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] >= 1
    assert len(data["deployments"]) >= 1