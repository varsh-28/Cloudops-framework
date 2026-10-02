def test_health_endpoint(api_client):
    """
    Verify the public application health endpoint.
    """

    response = api_client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "cloudops-service"
    assert "timestamp" in data


def test_service_health_endpoint(api_client, auth_headers):
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