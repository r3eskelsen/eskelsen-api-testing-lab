# Eskelsen Systems — Python API Testing & Automation Lab

Independent, synthetic FastAPI API testing demonstration.

## Scope

This repository demonstrates automated validation of a small inventory
REST API using Python, FastAPI, SQLAlchemy, pytest, HTTPX/TestClient,
SQLite fixtures, and pytest-cov.

Supported endpoints:

- GET /health
- POST /items
- GET /items
- GET /items/{item_id}
- PUT /items/{item_id}
- DELETE /items/{item_id}

Includes positive, negative, input validation, response contract,
CRUD persistence, and regression tests.

## Verified local results

Environment: Windows, Python 3.12.10.

- 45 tests passed
- 100% measured line and branch coverage of app/main.py
- 71 measured statements, 0 missing
- 8 measured branches, 0 partial branches
- One Starlette/TestClient deprecation warning

Results were independently re-executed on the local test environment.
A clean Python 3.12 virtual environment was created, dependencies were installed successfully, and all 45 tests passed again. GitHub Actions execution remains unverified.

Coverage is module-scoped, not a certification of system correctness.

## Setup

Create a Python 3.12 virtual environment.

Windows PowerShell:

    py -3.12 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

Linux/macOS:

    python3.12 -m venv .venv
    .venv/bin/python -m pip install -r requirements-dev.txt

## Run tests

Windows PowerShell:

    $env:DATABASE_URL='sqlite:///:memory:'
    .\.venv\Scripts\python.exe -m pytest tests -q --cov=app --cov-branch --cov-report=term-missing

Linux/macOS:

    DATABASE_URL=sqlite:///:memory: .venv/bin/python -m pytest tests -q --cov=app --cov-branch --cov-report=term-missing

## Reports

See TEST_PLAN.md, test_matrix.csv, QA_REPORT.md,
and docs/LIMITATIONS.md.

## Provenance

Based on the Eskelsen Systems FastAPI Backend Reference Demo,
upstream commit 75a244fd5c41661164d4f0942ab7b361041804ec.

This laboratory extends the demo with an isolated automated testing
suite and a PUT endpoint.

No client data or production systems were used.

## Licensing

Licensed under the MIT License. Copyright (c) 2026 Ralph Eskelsen (Eskelsen Systems). See LICENSE.
