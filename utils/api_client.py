from typing import Any

from fastapi.testclient import TestClient


class APIClient:
    """
    Reusable API wrapper around FastAPI TestClient.

    Generic get/post methods are intentionally exposed so existing
    tests remain backward compatible while newer tests can use
    higher-level methods.
    """

    def __init__(self, client: TestClient):
        self.client = client
        self.token: str | None = None

    # --------------------------------------------------------
    # Generic HTTP methods
    # --------------------------------------------------------

    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.client.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.client.put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.client.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.client.delete(*args, **kwargs)

    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------

    def login(
        self,
        username: str = "admin",
        password: str = "admin123",
    ):
        response = self.post(
            "/api/login",
            json={
                "username": username,
                "password": password,
            },
        )

        if response.status_code == 200:
            self.token = response.json()["access_token"]

        return response

    @property
    def auth_headers(self) -> dict[str, str]:
        if not self.token:
            raise RuntimeError(
                "Authentication required. Call login() first."
            )

        return {
            "Authorization": f"Bearer {self.token}"
        }

    # --------------------------------------------------------
    # Services
    # --------------------------------------------------------

    def get_services(self):
        return self.get(
            "/api/services",
            headers=self.auth_headers,
        )

    def get_service(self, service_name: str):
        return self.get(
            f"/api/services/{service_name}",
            headers=self.auth_headers,
        )

    def start_service(self, service_name: str):
        return self.post(
            f"/api/services/{service_name}/action",
            headers=self.auth_headers,
            json={"action": "start"},
        )

    def stop_service(self, service_name: str):
        return self.post(
            f"/api/services/{service_name}/action",
            headers=self.auth_headers,
            json={"action": "stop"},
        )

    def restart_service(self, service_name: str):
        return self.post(
            f"/api/services/{service_name}/action",
            headers=self.auth_headers,
            json={"action": "restart"},
        )

    def deploy_service_action(self, service_name: str):
        return self.post(
            f"/api/services/{service_name}/action",
            headers=self.auth_headers,
            json={"action": "deploy"},
        )

    # --------------------------------------------------------
    # Deployment
    # --------------------------------------------------------

    def deploy(
        self,
        service_name: str,
        version: str,
    ):
        return self.post(
            "/api/deploy",
            headers=self.auth_headers,
            json={
                "service_name": service_name,
                "version": version,
            },
        )

    def get_deployments(self):
        return self.get(
            "/api/deployments",
            headers=self.auth_headers,
        )

    def get_deployment_history(self):
        return self.get(
            "/api/deployments/history",
            headers=self.auth_headers,
        )

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    def health(self):
        return self.get("/health")

    def service_health(self):
        return self.get("/api/services/health")

    # --------------------------------------------------------
    # Current user
    # --------------------------------------------------------

    def get_current_user(self):
        return self.get(
            "/api/me",
            headers=self.auth_headers,
        )
