# CloudOps SDET Automation Framework

A Python-based Software Development Engineer in Test (SDET) automation framework designed to test a simulated CloudOps platform.

The project demonstrates API automation, UI automation, authentication testing, service management testing, deployment validation, negative testing, reporting, code coverage, and CI/CD integration.

---

## Project Overview

The framework contains a FastAPI-based CloudOps application and an automated test suite built using:

- Python
- Pytest
- FastAPI
- Playwright
- Pytest-Cov
- HTML reports
- JUnit reports
- GitHub Actions

---

## Architecture

```text
                    ┌──────────────────────┐
                    │   CloudOps FastAPI   │
                    │      Application     │
                    └──────────┬───────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
       ┌──────▼──────┐                  ┌──────▼──────┐
       │ API Tests   │                  │  UI Tests   │
       │   Pytest    │                  │ Playwright  │
       └──────┬──────┘                  └──────┬──────┘
              │                                 │
              └────────────────┬────────────────┘
                               │
                       ┌───────▼────────┐
                       │ Test Reporting │
                       │ HTML / JUnit   │
                       └───────┬────────┘
                               │
                       ┌───────▼────────┐
                       │ GitHub Actions │
                       │      CI        │
                       └────────────────┘

Features
Authentication
- Valid login
- Invalid username
- Invalid password
- Empty credentials
- Missing authentication header
- Invalid authentication scheme
- Invalid token
- Empty bearer token
- Current-user validation
Service Management
- Retrieve all services
- Retrieve individual service
- Start service
- Stop service
- Restart service
- Deploy service
- Invalid service action
- Non-existing service
Deployment
- Deploy service
- Unknown service deployment
- Deployment history
- Deployment validation
Health
- Application health
- Service health
UI
- Login page validation
- Dashboard validation
- Service information validation
Test Quality
- Positive testing
- Negative testing
- Parametrized testing
- API validation
- UI automation
- Authentication workflows
- Code coverage

Running the Application
Activate the virtual environment:
source .venv/bin/activate

Start the FastAPI application:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Application:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

Running Tests
Run all tests:
pytest -v

Run tests with coverage:
pytest -v --cov=app --cov-report=term-missing

Generate HTML coverage:
pytest -v --cov=app --cov-report=html

Run only API tests:
pytest tests/api -v

Run only UI tests:
pytest tests/ui -v

Reports
The framework generates:
reports/junit.xml
reports/report.html
htmlcov/

These reports provide:
- Test execution results
- Failed test information
- Test duration
- Code coverage
- CI-compatible JUnit output
CI/CD
GitHub Actions automatically executes the test suite on:
- Push to main/master
- Pull requests
The CI pipeline:
1. Checks out the repository
2. Installs Python
3. Installs dependencies
4. Installs Chromium
5. Executes API tests
6. Executes Playwright UI tests
7. Generates coverage
8. Generates JUnit reports
9. Uploads test artifacts
Test Statistics
Current local test baseline:
Tests:       39
Passed:      39
Failed:       0
Coverage:   100%
Warnings:     0

Technologies
Technology	Purpose
Python	Automation language
FastAPI	Demo application
Pytest	Test framework
Playwright	UI automation
Pytest-Cov	Code coverage
JUnit XML	CI test reporting
HTML Reports	Test reporting
GitHub Actions	CI/CD


Skills Demonstrated
This project demonstrates practical experience with:
- Python test automation
- API automation
- UI automation
- Pytest
- Playwright
- Fixtures
- Parametrization
- Authentication testing
- Negative testing
- REST APIs
- HTTP status validation
- Deployment testing
- Service testing
- Regression testing
- Code coverage
- Test reporting
- CI/CD
- GitHub Actions
- Linux
- Git
Future Improvements
Potential production-level extensions include:
- Docker-based execution
- Parallel test execution
- Allure reporting
- Environment-based configuration
- Secrets management
- API schema validation
- Database validation
- Kubernetes test execution
- Performance testing
- Test result notifications

---

# 5. Final local verification

Run these commands:

```bash
git status

Then:
pytest -v --cov=app --cov-report=term-missing