# API Test Plan

## Objective

Demonstrate reproducible functional and regression testing for
a synthetic FastAPI inventory API.

## Approach

- pytest with FastAPI TestClient
- isolated SQLite in-memory test database
- fixture-controlled dependency injection
- positive and negative API scenarios
- Pydantic input validation
- HTTP status and response contract assertions
- CRUD persistence and not-found behavior
- line and branch coverage using pytest-cov

## Scope

Health endpoint and inventory CRUD endpoints.

The scenario design matrix is provided in test_matrix.csv.
Its 35 design scenarios are not equivalent to 35 individual pytest
functions. Executed pytest counts are documented separately.

## Acceptance

- No tests run against production services
- No real customer information
- All pytest tests pass
- Measured application coverage is at least 85%
- Source reference remains unchanged
- Known warnings and limitations are documented

## Exclusions

- Performance/load certification
- Production security certification
- Real authentication or authorization
- Docker/PostgreSQL integration testing
- Browser E2E testing
- Production deployment

## Evidence

Results are based on local Windows execution and retained in the
private laboratory evidence directory. Public claims must not imply
CI verification until a real GitHub Actions run is inspected.
