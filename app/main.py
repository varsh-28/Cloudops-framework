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
# DATA
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
# HELPERS
# ============================================================

def current_timestamp():
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_token(authorization: str | None):

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
# LOGIN PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def root():

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

            #login-success-message {
                margin-top: 15px;
                text-align: center;
                color: green;
            }

            #login-error-message {
                margin-top: 15px;
                text-align: center;
                color: red;
            }

            #dashboard-button {
                display: none;
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


                <button
                    type="submit"
                >
                    Login
                </button>

            </form>


            <div id="login-success-message"></div>


            <div id="login-error-message"></div>


            <button
                id="dashboard-button"
                type="button"
                onclick="window.location.href='/dashboard';"
            >
                Open Dashboard
            </button>

        </div>


        <script>

            document
                .getElementById("login-form")
                .addEventListener(
                    "submit",
                    async function(event) {

                        event.preventDefault();


                        const username =
                            document.getElementById(
                                "username"
                            ).value;


                        const password =
                            document.getElementById(
                                "password"
                            ).value;


                        const successMessage =
                            document.getElementById(
                                "login-success-message"
                            );


                        const errorMessage =
                            document.getElementById(
                                "login-error-message"
                            );


                        const dashboardButton =
                            document.getElementById(
                                "dashboard-button"
                            );


                        successMessage.innerText = "";
                        errorMessage.innerText = "";

                        dashboardButton.style.display = "none";


                        try {

                            const response =
                                await fetch(
                                    "/api/login",
                                    {
                                        method: "POST",

                                        headers: {
                                            "Content-Type":
                                                "application/json"
                                        },

                                        body: JSON.stringify({
                                            username: username,
                                            password: password
                                        })
                                    }
                                );


                            const data =
                                await response.json();


                            if (response.ok) {

                                successMessage.innerText =
                                    `Login successful. Welcome ${data.username}.`;


                                dashboardButton.style.display =
                                    "block";

                            } else {

                                errorMessage.innerText =
                                    data.detail ||
                                    "Login failed";

                            }

                        } catch (error) {

                            errorMessage.innerText =
                                "Unable to connect to server";

                        }

                    }
                );

        </script>

    </body>

    </html>
    """


# ============================================================
# DASHBOARD
# ============================================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    rows = ""

    for service in SERVICES.values():

        rows += f"""
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

            th,
            td {{
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

                {rows}

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

    return {
        "status": "healthy",
        "service": "cloudops-service",
        "timestamp": current_timestamp(),
    }


@app.get("/api/services/health")
def service_health():

    return {
        "status": "healthy",
        "service": "cloudops-service",
        "services": len(SERVICES),
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
# SERVICES
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
    authorization: str | None = Header(default=None),
):

    user = validate_token(authorization)

    service = SERVICES.get(service_name)


    if not service:

        raise HTTPException(
            status_code=404,
            detail="Service not found",
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
# DEPLOYMENT
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
            detail="Service not found",
        )


    deployment_id = str(uuid4())

    timestamp = current_timestamp()


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


    return {
        "message": (
            f"Deployment of "
            f"{request.service_name} "
            f"version {request.version} successful"
        ),

        "deployment": deployment,

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