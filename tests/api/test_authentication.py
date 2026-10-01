import pytest

from tests.data.auth_test_data import AUTH_TEST_CASES


@pytest.mark.parametrize(
    "test_case",
    AUTH_TEST_CASES,
    ids=[case["name"] for case in AUTH_TEST_CASES],
)
def test_login_scenarios(api_client, test_case):
    response = api_client.post(
        "/api/login",
        json={
            "username": test_case["username"],
            "password": test_case["password"],
        },
    )

    assert response.status_code == test_case["expected_status"]

    data = response.json()

    if test_case["expected_success"]:
        assert "token" in data
        assert data["username"] == test_case["username"]
        assert "role" in data
    else:
        assert "token" not in data