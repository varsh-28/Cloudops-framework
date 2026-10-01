import os


BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000"
)

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "qa"
)

API_TIMEOUT = int(
    os.getenv(
        "API_TIMEOUT",
        "10"
    )
)
