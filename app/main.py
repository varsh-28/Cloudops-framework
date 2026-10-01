from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI(
    title="CloudOps SDET Test API",
    description="Demo CloudOps service used for API and UI automation testing",
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
    }
}


SERVICES = {
    "payment-service": {
        "name": "payment-service",
        "status": "running",
        "version": "1.0.0",
        "environment": "qa",
    },
    "user-service": {
        "name": "user-service",
        "status": "running",
        "version": "1.0.0",
        "environment": "qa",
    },
    "order-service": {
        "name": "order-service",
        "status": "running",
        "version": "1.0.0",
        "environment": "qa",
    },
}


DEPLOYMENTS = []

# token -> username
ACTIVE_TOKENS = {}


# ============================================================
# PYDANTIC MODELS
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
# HELPERS
# ============================================================

def current_timestamp():
    """
    Return the current UTC timestamp in ISO-8601 format.
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_token(authorization: str | None):
    """
    Validate a Bearer token and return the authenticated user.
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme",
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    username = ACTIVE_TOKENS.get(token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token",
        )

    user = USERS.get(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


# ============================================================
# ROOT / UI
# ============================================================

@app.get("/", response_class=HTMLResponse)
def root():
    """
    Simple login page used by Playwright UI tests.
    """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudOps SDET Framework</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 40px;
            }

            .container {
                width: 400px;
                margin: 80px auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            h1 {
                text-align: center;
                color: #222;
            }

            input {
                width: 100%;
                padding: 12px;
                margin: 8px 0;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            button:hover {
                background: #1d4ed8;
            }

            #message {
                margin-top: 15px;
                text-align: center;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>CloudOps Login</h1>

            <form id="login-form">

                <input
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Username"
                    required
                >

                <input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Password"
                    required
                >

                <button type="submit">
                    Login
                </button>

            </form>

            <div id="message"></div>

        </div>


        <script>

            document
                .getElementById("login-form")
                .addEventListener("submit", async function(event) {

                    event.preventDefault();

                    const username =
                        document.getElementById("username").value;

                    const password =
                        document.getElementById("password").value;

                    const response = await fetch("/api/login", {

                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            username: username,
                            password: password
                        })

                    });

                    const data = await response.json();

                    const message =
                        document.getElementById("message");

                    if (response.ok) {

                        message.innerText =
                            "Login successful";

                        message.style.color = "green";

                    } else {

                        message.innerText =
                            data.detail || "Login failed";

                        message.style.color = "red";
                    }

                });

        </script>

    </body>
    </html>
    """


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """
    Simple dashboard endpoint.
    """

    service_rows = ""

    for service in SERVICES.values():

        service_rows += f"""
        <tr>
            <td>{service["name"]}</td>
            <td>{service["status"]}</td>
            <td>{service["version"]}</td>
            <td>{service["environment"]}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudOps Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
            }}

            th {{
                background: #f2f2f2;
            }}
        </style>
    </head>

    <body>

        <h1>CloudOps Dashboard</h1>

        <table>

            <thead>
                <tr>
                    <th>Service</th>
                    <th>Status</th>
                    <th>Version</th>
                    <th>Environment</th>
                </tr>
            </thead>

            <tbody>
                {service_rows}
            </tbody>

        </table>

    </body>
    </html>
    """


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    """
    Application health endpoint.
    """

    return {
        "status": "healthy",
        "service": "cloudops-service",
        "timestamp": current_timestamp(),
    }


# ============================================================
# AUTHENTICATION
# ============================================================

@app.post("/api/login")
def login(request: LoginRequest):

    user = USERS.get(request.username)

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if user["password"] != request.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = str(uuid4())

    ACTIVE_TOKENS[token] = user["username"]

    return {
        "message": "Login successful",
        "token": token,
        "access_token": token,
        "username": user["username"],
        "role": user["role"],
    }


# ============================================================
# CURRENT USER
# ============================================================

@app.get("/api/me")
def get_current_user(
    authorization: str | None = Header(default=None),
):

    user = validate_token(authorization)

    return {
        "username": user["username"],
        "role": user["role"],
    }


# ============================================================
# SERVICE HEALTH
# ============================================================

@app.get("/api/services/health")
def service_health():

    return {
        "status": "healthy",
        "service": "cloudops-service",
        "services": len(SERVICES),
    }


# ============================================================
# GET ALL SERVICES
# ============================================================

@app.get("/api/services")
def get_all_services(
    authorization: str | None = Header(default=None),
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
    authorization: str | None = Header(default=None),
):

    validate_token(authorization)

    service = SERVICES.get(service_name)

    if not service:

        raise HTTPException(
            status_code=404,
            detail=f"Service '{service_name}' not found",
        )

    return service


# ============================================================
# SERVICE ACTION
# ============================================================

@app.post("/api/services/{service_name}/action")
def service_action(
    service_name: str,
    request: ServiceActionRequest,
    authorization: str | None = Header(default=None),
):

    user = validate_token(authorization)

    service = SERVICES.get(service_name)

    if not service:

        raise HTTPException(
            status_code=404,
            detail=f"Service '{service_name}' not found",
        )

    allowed_actions = {
        "start",
        "stop",
        "restart",
        "deploy",
    }

    if request.action not in allowed_actions:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid action. "
                f"Allowed actions: {sorted(allowed_actions)}"
            ),
        )

    if request.action == "start":

        service["status"] = "running"

    elif request.action == "stop":

        service["status"] = "stopped"

    elif request.action == "restart":

        service["status"] = "running"

    elif request.action == "deploy":

        service["status"] = "running"

    return {
        "message": (
            f"{service_name} "
            f"{request.action} successful"
        ),
        "service": service,
        "performed_by": user["username"],
    }


# ============================================================
# DEPLOY SERVICE
# ============================================================

@app.post("/api/deploy")
def deploy_service(
    request: DeploymentRequest,
    authorization: str | None = Header(default=None),
):

    user = validate_token(authorization)

    service = SERVICES.get(request.service_name)

    if not service:

        raise HTTPException(
            status_code=404,
            detail=f"Service '{request.service_name}' not found",
        )

    deployment_id = str(uuid4())

    timestamp = current_timestamp()

    # Update service state
    service["version"] = request.version
    service["status"] = "running"

    deployment = {
        "deployment_id": deployment_id,
        "service_name": request.service_name,
        "version": request.version,
        "environment": "qa",
        "status": "successful",
        "deployed_by": user["username"],
        "timestamp": timestamp,
    }

    DEPLOYMENTS.append(deployment)

    # IMPORTANT:
    # The test suite expects the deployment response
    # to contain a "message" field.
    return {
        "message": (
            f"Deployment of "
            f"{request.service_name} "
            f"version {request.version} successful"
        ),
        **deployment,
    }


# ============================================================
# DEPLOYMENT HISTORY
# ============================================================

@app.get("/api/deployments")
def get_deployments(
    authorization: str | None = Header(default=None),
):

    validate_token(authorization)

    return {
        "count": len(DEPLOYMENTS),
        "deployments": DEPLOYMENTS,
    }


@app.get("/api/deployments/history")
def deployment_history(
    authorization: str | None = Header(default=None),
):

    validate_token(authorization)

    return {
        "count": len(DEPLOYMENTS),
        "deployments": DEPLOYMENTS,
    }


# ============================================================
# APPLICATION INFO
# ============================================================

@app.get("/api/info")
def application_info():

    return {
        "application": "CloudOps SDET Framework",
        "version": "1.0.0",
        "environment": "qa",
        "service_count": len(SERVICES),
        "deployment_count": len(DEPLOYMENTS),
    }