from __future__ import annotations

from typing import Any


class APIClient:
    """
    Reusable API client wrapper around FastAPI TestClient.
    """

    def __init__(self, client):
        self.client = client
        self.token: str | None = None
        self.username: str | None = None

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    def login(
        self,
        username: str = "admin",
        password: str = "admin123",
    ):
        response = self.client.post(
            "/api/login",
            json={
                "username": username,
                "password": password,
            },
        )

        if response.status_code == 200:
            data = response.json()

            self.token = (
                data.get("access_token")
                or data.get("token")
            )

            self.username = data.get(
                "username",
                username,
            )

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

    # ============================================================
    # BASIC HTTP METHODS
    # ============================================================

    def get(
        self,
        endpoint: str,
        *,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ):
        return self.client.get(
            endpoint,
            headers=headers,
            **kwargs,
        )

    def post(
        self,
        endpoint: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        return self.client.post(
            endpoint,
            headers=headers,
            json=json,
            **kwargs,
        )

    # ============================================================
    # HEALTH
    # ============================================================

    def health(self):
        """
        Public application health endpoint.
        """
        return self.get("/health")

    def service_health(self):
        """
        Public service health endpoint.

        No authentication is required because
        /api/services/health is intentionally public
        in app/main.py.
        """
        return self.get("/api/services/health")

    def get_service_health(self):
        return self.service_health()

    # ============================================================
    # SERVICES
    # ============================================================

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

    def service_action(
        self,
        service_name: str,
        action: str,
    ):
        return self.post(
            f"/api/services/{service_name}/action",
            headers=self.auth_headers,
            json={
                "action": action,
            },
        )

    # ============================================================
    # DEPLOYMENT
    # ============================================================

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

    # ============================================================
    # CURRENT USER
    # ============================================================

    def get_current_user(self):
        return self.get(
            "/api/me",
            headers=self.auth_headers,
        )

    # ============================================================
    # LOGOUT
    # ============================================================

    def logout(self):
        """
        Clear locally stored authentication state.
        """
        self.token = None
        self.username = None