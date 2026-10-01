from typing import Any

from starlette.testclient import TestClient


class APIClient:
    """
    Reusable wrapper around FastAPI TestClient.

    Keeps API calls consistent across the test suite.
    """

    def __init__(self, client: TestClient):
        self.client = client

    def get(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ):
        return self.client.get(
            endpoint,
            headers=headers,
            params=params,
        )

    def post(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ):
        return self.client.post(
            endpoint,
            headers=headers,
            json=json,
        )

    def put(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ):
        return self.client.put(
            endpoint,
            headers=headers,
            json=json,
        )

    def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ):
        return self.client.delete(
            endpoint,
            headers=headers,
        )
