AUTH_TEST_CASES = [
    {
        "name": "valid_admin",
        "username": "admin",
        "password": "admin123",
        "expected_status": 200,
        "expected_success": True,
    },
    {
        "name": "invalid_password",
        "username": "admin",
        "password": "wrongpassword",
        "expected_status": 401,
        "expected_success": False,
    },
    {
        "name": "invalid_username",
        "username": "unknown_user",
        "password": "admin123",
        "expected_status": 401,
        "expected_success": False,
    },
]
