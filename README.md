# CloudOps SDET Automation Framework

A Python-based **Software Development Engineer in Test (SDET) automation framework** designed to validate a simulated CloudOps platform through API and UI automation.

The project demonstrates practical automation engineering across **REST API testing, UI testing, authentication, service management, deployment validation, negative testing, test reporting, code coverage, and CI/CD integration**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Application Features](#application-features)
- [Test Coverage](#test-coverage)
- [Test Design](#test-design)
- [Running the Application](#running-the-application)
- [Running the Test Suite](#running-the-test-suite)
- [Test Reports](#test-reports)
- [CI/CD Pipeline](#cicd-pipeline)
- [Quality Gates](#quality-gates)
- [Current Verification](#current-verification)
- [Skills Demonstrated](#skills-demonstrated)
- [Future Enhancements](#future-enhancements)
- [Final Verification](#final-verification)
- [Project Summary](#project-summary)

---

## Project Overview

The **CloudOps SDET Automation Framework** combines a lightweight FastAPI application with an automated testing framework built using Pytest and Playwright.

The simulated application provides CloudOps-style functionality such as:

- Authentication
- Service health monitoring
- Service management
- Service actions
- Deployments
- Deployment history
- Application information
- Web dashboard

The automation framework validates these capabilities through API and browser-based tests.

---

## Objectives

The project was designed to demonstrate an end-to-end SDET workflow:

1. Build a testable CloudOps application.
2. Design reusable API automation utilities.
3. Automate authentication workflows.
4. Validate REST API responses and HTTP status codes.
5. Automate browser workflows using Playwright.
6. Implement positive and negative test scenarios.
7. Use fixtures and parametrization for reusable tests.
8. Generate JUnit and HTML test reports.
9. Measure application code coverage.
10. Execute the complete test suite through GitHub Actions.

---

## Architecture

```text
                         +--------------------------+
                         |     CloudOps FastAPI     |
                         |       Application        |
                         +------------+-------------+
                                      |
                    +-----------------+-----------------+
                    |                                   |
             +------+-------+                    +------+-------+
             |   API Tests  |                    |   UI Tests  |
             |    Pytest    |                    |  Playwright |
             +------+-------+                    +------+-------+
                    |                                   |
                    +-----------------+-----------------+
                                      |
                             +--------+--------+
                             | Test Execution  |
                             |     Pytest      |
                             +--------+--------+
                                      |
                       +--------------+--------------+
                       |                             |
                +------+-------+             +-------+------+
                | HTML Report  |             |  JUnit XML   |
                |              |             |    Report    |
                +--------------+             +--------------+
                                      |
                             +--------+--------+
                             | GitHub Actions |
                             |      CI/CD     |
                             +-----------------+
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Automation and application development |
| FastAPI | Simulated CloudOps REST application |
| Pytest | Test execution and test framework |
| Playwright | Browser/UI automation |
| Pytest-Cov | Code coverage measurement |
| HTML Reports | Human-readable test reporting |
| JUnit XML | CI-compatible test reporting |
| GitHub Actions | Continuous Integration |
| Git | Source control |
| Linux/WSL | Development and execution environment |

---

## Project Structure

```text
cloudops-sdet-framework/
|
+-- app/
|   +-- __init__.py
|   +-- main.py
|
+-- tests/
|   +-- api/
|   |   +-- test_application.py
|   |   +-- test_authentication.py
|   |   +-- test_deployments.py
|   |   +-- test_health.py
|   |   +-- test_services.py
|   |
|   +-- ui/
|       +-- test_login.py
|
+-- utils/
|   +-- api_client.py
|
+-- reports/
|   +-- junit.xml
|   +-- report.html
|
+-- htmlcov/
|   +-- ...
|
+-- .github/
|   +-- workflows/
|       +-- ...
|
+-- pytest.ini
+-- requirements.txt
+-- README.md
```

---

# Application Features

## 1. Authentication

The application supports token-based authentication for protected API operations.

Implemented scenarios include:

- Valid login
- Invalid username
- Invalid password
- Empty username
- Empty password
- Missing authentication header
- Invalid authentication scheme
- Invalid authentication token
- Empty bearer token
- Current-user validation

Authentication flow:

```text
Login
  |
  v
Credentials validated
  |
  v
Access token generated
  |
  v
Token supplied in Authorization header
  |
  v
Protected endpoint accessed
```

---

## 2. Service Management

The framework validates CloudOps service operations including:

- Retrieve all services
- Retrieve an individual service
- Start a service
- Stop a service
- Restart a service
- Deploy a service
- Validate invalid service actions
- Validate non-existing services

Supported service actions:

```text
start
stop
restart
deploy
```

---

## 3. Deployment Management

Deployment functionality includes:

- Service deployment
- Version validation
- Unknown service validation
- Deployment status validation
- Deployment history validation
- Deployment metadata validation

A deployment records information such as:

```text
Deployment ID
Service Name
Version
Environment
Status
Deployed By
Timestamp
```

---

## 4. Health Monitoring

Health endpoints are validated through automated API tests.

Implemented endpoints include:

```text
GET /health
GET /api/services/health
```

The tests verify that the application and service layer report a healthy state.

---

## 5. Web Dashboard

A browser-accessible dashboard displays service information including:

- Service name
- Service status
- Service version
- Environment

The dashboard is validated using Playwright.

---

# Test Coverage

The test suite contains API and UI automation.

## Authentication Tests

```text
Valid credentials
Invalid credentials
Empty credentials
Missing authentication
Invalid authentication scheme
Invalid token
Empty bearer token
Current-user endpoint
```

## Service Tests

```text
Get all services
Get individual service
Start service
Stop service
Restart service
Deploy service
Invalid service action
Unknown service
Authentication enforcement
Service health
Deployment history
```

## Deployment Tests

```text
Successful deployment
Unknown service deployment
Deployment history
Deployment validation
```

## Health Tests

```text
Application health
Service health
```

## UI Tests

```text
Login page
Valid login
Dashboard rendering
Service information display
```

---

# Test Design

The framework uses standard SDET practices.

### Positive Testing

Valid requests are tested to confirm expected application behavior.

### Negative Testing

Invalid inputs and invalid states are tested to verify correct error handling.

### Parametrization

Related scenarios are grouped using Pytest parametrization to reduce duplicated test code.

### Fixtures

Reusable setup and test dependencies are managed through Pytest fixtures.

### API Client Abstraction

The reusable API client separates HTTP interaction from test logic.

Conceptual flow:

```text
Test
 |
 v
APIClient
 |
 v
HTTP Request
 |
 v
FastAPI Application
 |
 v
Response
 |
 v
Assertions
```

---

# Running the Application

## 1. Activate the virtual environment

```bash
source .venv/bin/activate
```

Verify Python:

```bash
python --version
```

---

## 2. Start the FastAPI application

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Application:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Running the Test Suite

## Run all tests

```bash
pytest -v
```

## Run tests with coverage

```bash
pytest -v --cov=app --cov-report=term-missing
```

## Generate HTML coverage

```bash
pytest -v --cov=app --cov-report=html
```

The generated coverage report is available under:

```text
htmlcov/
```

## Run only API tests

```bash
pytest tests/api -v
```

## Run only UI tests

```bash
pytest tests/ui -v
```

## Run a specific test file

```bash
pytest tests/api/test_authentication.py -v
```

## Run a specific test

```bash
pytest tests/api/test_health.py::test_health_endpoint -v
```

---

# Test Reports

The framework generates CI-compatible and human-readable reports.

## JUnit XML

```text
reports/junit.xml
```

Suitable for:

- GitHub Actions
- CI servers
- Test result dashboards
- Automated result processing

## HTML Test Report

```text
reports/report.html
```

Provides:

- Test execution status
- Passed/failed tests
- Test duration
- Test details

## HTML Coverage Report

```text
htmlcov/
```

Provides:

- Statement coverage
- Missing lines
- File-level coverage
- Overall coverage percentage

---

# CI/CD Pipeline

GitHub Actions executes the test suite through the project's CI workflow.

Pipeline flow:

```text
Git Push / Pull Request
          |
          v
Checkout Repository
          |
          v
Setup Python
          |
          v
Install Dependencies
          |
          v
Install Playwright Chromium
          |
          v
Run Automated Tests
          |
          v
Generate Coverage
          |
          v
Generate JUnit Report
          |
          v
Upload Test Artifacts
```

The CI pipeline validates the project consistently in an automated environment.

---

# Quality Gates

The project uses automated test execution and coverage as quality indicators.

A successful validation requires:

```text
All tests passing
        +
No test failures
        +
Expected coverage maintained
        +
Reports generated successfully
```

---

# Current Verification

Latest local verification:

```text
Tests:       39
Passed:      39
Failed:       0
Coverage:   100%
Warnings:     0
```

Command:

```bash
pytest -v --cov=app --cov-report=term-missing
```

Expected successful result:

```text
39 passed
100% coverage
```

---

# Skills Demonstrated

## Python

- Python test automation
- Functions and classes
- Exception handling
- API client development
- Test utilities

## API Automation

- REST API testing
- HTTP status validation
- Request/response validation
- Authentication workflows
- Negative testing
- Endpoint validation

## Pytest

- Fixtures
- Parametrization
- Assertions
- Test organization
- Test discovery
- Coverage integration

## Playwright

- Browser automation
- UI validation
- Login workflow testing
- Dashboard validation
- Chromium execution

## SDET Practices

- Positive testing
- Negative testing
- Regression testing
- Authentication testing
- Reusable test architecture
- Test reporting
- Code coverage
- CI/CD integration

## DevOps / CloudOps

- Service lifecycle testing
- Deployment validation
- Health monitoring validation
- Linux/WSL environment
- Git workflows
- GitHub Actions

---

# Future Enhancements

Potential production-level extensions include:

## Test Framework

- Parallel test execution
- Allure reporting
- Environment-based configuration
- API schema validation
- Contract testing
- Improved test data management

## Infrastructure

- Docker-based test execution
- Kubernetes-based test execution
- Cloud environment integration

## Security

- Secrets management
- Environment variables for credentials
- Token lifecycle testing
- Role-based authorization testing

## Data Validation

- Database validation
- Backend state verification
- Deployment state persistence

## Performance

- API performance testing
- Load testing
- Response-time thresholds

## CI/CD

- Test result notifications
- Pull request quality gates
- Scheduled regression execution
- Multi-environment testing

---

# Final Verification

Before committing changes:

```bash
git status
```

Run the complete validation:

```bash
pytest -v --cov=app --cov-report=term-missing
```

Verify:

```text
All tests PASS
Coverage is maintained
No unexpected failures
Reports are generated
```

Then:

```bash
git status
git add .
git commit -m "Complete CloudOps SDET automation framework"
git push origin main
```

---

# Project Summary

The **CloudOps SDET Automation Framework** demonstrates an end-to-end automated testing workflow around a simulated CloudOps platform.

It combines:

```text
Python
   +
FastAPI
   +
Pytest
   +
Playwright
   +
API Automation
   +
UI Automation
   +
Authentication Testing
   +
Deployment Testing
   +
Negative Testing
   +
Code Coverage
   +
Test Reporting
   +
GitHub Actions
```

The project provides a practical portfolio example of how an SDET can design, automate, validate, report, and continuously execute a modern software testing framework.
