from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app = FastAPI(
    title="CloudOps Service",
    description="CloudOps application for SDET automation testing",
    version="1.0.0",
)


# ============================================================
# IN-MEMORY DATA
# ============================================================

USERS = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin",
    },
    "tester": {
        "username": "tester",
        "password": "tester123",
        "role": "tester",
    },
}


SERVICES = {
    "payment-service": {
        "name": "payment-service",
        "version": "2.4.1",
        "status": "running",
        "environment": "qa",
        "port": 8081,
    },
    "user-service": {
        "name": "user-service",
        "version": "1.8.3",
        "status": "running",
        "environment": "qa",
        "port": 8082,
    },
    "notification-service": {
        "name": "notification-service",
        "version": "3.1.0",
        "status": "running",
        "environment": "qa",
        "port": 8083,
    },
}


DEPLOYMENTS = []

ACTIVE_TOKENS = {}


# ============================================================
# REQUEST MODELS
# ============================================================

class LoginRequest(BaseModel):
    username: str
    password: str


class DeploymentRequest(BaseModel):
    service_name: str
    version: str


class ServiceActionRequest(BaseModel):
    action: str


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_current_time():
    return datetime.utcnow().isoformat() + "Z"


def authenticate_user(username: str, password: str):
    user = USERS.get(username)

    if not user:
        return None

    if user["password"] != password:
        return None

    return user


def validate_token(authorization: Optional[str]):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format",
        )

    token = authorization.replace("Bearer ", "", 1)

    username = ACTIVE_TOKENS.get(token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    return USERS[username]


# ============================================================
# WEB APPLICATION / LOGIN PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>CloudOps Service</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 40px;
            }

            .container {
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }

            h1 {
                color: #1f2937;
            }

            h2 {
                color: #374151;
            }

            .status {
                padding: 15px;
                background: #dcfce7;
                color: #166534;
                border-radius: 6px;
                margin: 20px 0;
            }

            input {
                display: block;
                width: 300px;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #d1d5db;
                border-radius: 5px;
            }

            button {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            .login-button {
                background: #2563eb;
                color: white;
            }

            .dashboard-button {
                background: #16a34a;
                color: white;
                margin-top: 20px;
            }

            .error {
                color: #dc2626;
                margin-top: 10px;
            }

            .success {
                color: #166534;
                margin-top: 10px;
            }

            .endpoint {
                padding: 12px;
                background: #f3f4f6;
                margin: 8px 0;
                border-radius: 5px;
            }

            a {
                color: #2563eb;
                text-decoration: none;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>CloudOps Service</h1>

            <div class="status">
                Application is running
            </div>

            <h2>Login</h2>

            <input
                id="username"
                type="text"
                placeholder="Username"
            />

            <input
                id="password"
                type="password"
                placeholder="Password"
            />

            <button
                id="login-button"
                class="login-button"
                onclick="login()"
            >
                Login
            </button>

            <div
                id="login-error"
                class="error"
            ></div>

            <div
                id="login-success"
                class="success"
            ></div>

            <h2>Available Endpoints</h2>

            <div class="endpoint">
                GET /health
            </div>

            <div class="endpoint">
                POST /api/login
            </div>

            <div class="endpoint">
                GET /api/services
            </div>

            <div class="endpoint">
                GET /api/services/{service_name}
            </div>

            <div class="endpoint">
                POST /api/services/{service_name}/action
            </div>

            <div class="endpoint">
                POST /api/deploy
            </div>

            <div class="endpoint">
                GET /api/deployments
            </div>

            <p>
                <a href="/docs">
                    Open Swagger API Documentation
                </a>
            </p>

        </div>

        <script>

            async function login() {

                const username =
                    document.getElementById("username").value;

                const password =
                    document.getElementById("password").value;

                const errorElement =
                    document.getElementById("login-error");

                const successElement =
                    document.getElementById("login-success");

                errorElement.textContent = "";
                successElement.innerHTML = "";

                try {

                    const response = await fetch(
                        "/api/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type": "application/json"
                            },

                            body: JSON.stringify({
                                username: username,
                                password: password
                            })
                        }
                    );

                    const data = await response.json();

                    if (!response.ok) {

                        errorElement.textContent =
                            data.detail;

                        return;
                    }

                    sessionStorage.setItem(
                        "authToken",
                        data.token
                    );

                    successElement.innerHTML =
                        "<p id='login-success-message'>" +
                        "Login successful. Welcome " +
                        data.username +
                        ".</p>" +
                        "<button " +
                        "id='dashboard-button' " +
                        "class='dashboard-button' " +
                        "onclick='openDashboard()'>" +
                        "Open Dashboard" +
                        "</button>";

                } catch (error) {

                    errorElement.textContent =
                        "Unable to connect to server.";

                }
            }


            function openDashboard() {

                window.location.href = "/dashboard";

            }

        </script>

    </body>

    </html>
    """


# ============================================================
# DASHBOARD
# ============================================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>CloudOps Dashboard</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 40px;
            }

            .container {
                max-width: 1100px;
                margin: auto;
            }

            .header {
                background: white;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 20px;
            }

            .services {
                display: grid;
                grid-template-columns:
                    repeat(3, 1fr);
                gap: 20px;
            }

            .service {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow:
                    0 2px 8px rgba(0,0,0,0.08);
            }

            .running {
                color: #16a34a;
                font-weight: bold;
            }

            .stopped {
                color: #dc2626;
                font-weight: bold;
            }

            button {
                padding: 8px 15px;
                margin-top: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            .refresh {
                background: #2563eb;
                color: white;
            }

            .logout {
                background: #dc2626;
                color: white;
            }

            #message {
                margin: 15px 0;
                font-weight: bold;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <div class="header">

                <h1>CloudOps Dashboard</h1>

                <p>
                    Environment:
                    <strong>QA</strong>
                </p>

                <button
                    id="refresh-button"
                    class="refresh"
                    onclick="loadServices()"
                >
                    Refresh Services
                </button>

                <button
                    id="logout-button"
                    class="logout"
                    onclick="logout()"
                >
                    Logout
                </button>

                <div id="message"></div>

            </div>

            <div
                id="services"
                class="services"
            ></div>

        </div>


        <script>

            async function loadServices() {

                const token =
                    sessionStorage.getItem("authToken");

                if (!token) {

                    window.location.href = "/";

                    return;
                }

                const response = await fetch(
                    "/api/services",
                    {
                        headers: {
                            "Authorization":
                                "Bearer " + token
                        }
                    }
                );

                if (response.status === 401) {

                    sessionStorage.removeItem(
                        "authToken"
                    );

                    window.location.href = "/";

                    return;
                }

                const data = await response.json();

                const container =
                    document.getElementById("services");

                container.innerHTML = "";

                data.services.forEach(service => {

                    const card =
                        document.createElement("div");

                    card.className = "service";

                    const statusClass =
                        service.status === "running"
                            ? "running"
                            : "stopped";

                    card.innerHTML = `

                        <h2
                            data-testid="service-name"
                        >
                            ${service.name}
                        </h2>

                        <p>
                            Version:
                            <strong>
                                ${service.version}
                            </strong>
                        </p>

                        <p>
                            Environment:
                            ${service.environment}
                        </p>

                        <p>
                            Port:
                            ${service.port}
                        </p>

                        <p>
                            Status:
                            <span
                                class="${statusClass}"
                                data-testid="service-status"
                            >
                                ${service.status}
                            </span>
                        </p>

                    `;

                    container.appendChild(card);

                });

            }


            function logout() {

                sessionStorage.removeItem(
                    "authToken"
                );

                window.location.href = "/";

            }


            loadServices();

        </script>

    </body>

    </html>
    """


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "cloudops-service",
        "timestamp": get_current_time(),
    }


# ============================================================
# LOGIN API
# ============================================================

@app.post("/api/login")
def login(request: LoginRequest):

    user = authenticate_user(
        request.username,
        request.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = str(uuid4())

    ACTIVE_TOKENS[token] = user["username"]

    return {
        "message": "Login successful",
        "token": token,
        "username": user["username"],
        "role": user["role"],
    }


# ============================================================
# CURRENT USER
# ============================================================

@app.get("/api/me")
def current_user(
    authorization: Optional[str] = Header(default=None)
):

    user = validate_token(authorization)

    return {
        "username": user["username"],
        "role": user["role"],
    }


# ============================================================
# GET ALL SERVICES
# ============================================================

@app.get("/api/services")
def get_services(
    authorization: Optional[str] = Header(default=None)
):

    validate_token(authorization)

    return {
        "count": len(SERVICES),
        "services": list(SERVICES.values()),
    }


# ============================================================
# GET INDIVIDUAL SERVICE
# ============================================================

@app.get("/api/services/{service_name}")
def get_service(
    service_name: str,
    authorization: Optional[str] = Header(default=None),
):

    validate_token(authorization)

    service = SERVICES.get(service_name)

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    return service


# ============================================================
# SERVICE ACTION
# ============================================================

@app.post("/api/services/{service_name}/action")
def service_action(
    service_name: str,
    request: ServiceActionRequest,
    authorization: Optional[str] = Header(default=None),
):

    validate_token(authorization)

    service = SERVICES.get(service_name)

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    allowed_actions = [
        "start",
        "stop",
        "restart",
    ]

    if request.action not in allowed_actions:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid action. "
                f"Allowed actions: {allowed_actions}"
            ),
        )

    if request.action == "start":
        service["status"] = "running"

    elif request.action == "stop":
        service["status"] = "stopped"

    elif request.action == "restart":
        service["status"] = "running"

    return {
        "message": (
            f"{service_name} "
            f"{request.action} successful"
        ),
        "service": service,
    }


# ============================================================
# DEPLOY SERVICE
# ============================================================

@app.post("/api/deploy")
def deploy_service(
    request: DeploymentRequest,
    authorization: Optional[str] = Header(default=None),
):

    user = validate_token(authorization)

    service = SERVICES.get(request.service_name)

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    deployment = {
        "deployment_id": str(uuid4()),
        "service_name": request.service_name,
        "version": request.version,
        "environment": "qa",
        "status": "successful",
        "deployed_by": user["username"],
        "timestamp": get_current_time(),
    }

    service["version"] = request.version
    service["status"] = "running"

    DEPLOYMENTS.append(deployment)

    return deployment


# ============================================================
# DEPLOYMENT HISTORY
# ============================================================

@app.get("/api/deployments")
def get_deployments(
    authorization: Optional[str] = Header(default=None)
):

    validate_token(authorization)

    return {
        "count": len(DEPLOYMENTS),
        "deployments": DEPLOYMENTS,
    }


# ============================================================
# APPLICATION INFORMATION
# ============================================================

@app.get("/api/info")
def application_info():

    return {
        "application": "CloudOps Service",
        "version": "1.0.0",
        "environment": "qa",
        "services": len(SERVICES),
        "features": [
            "authentication",
            "health monitoring",
            "service management",
            "deployment management",
            "deployment history",
        ],
    }