# QA Report

Project: ESK-LAB-05
Status: Locally verified; public release pending
Date of local validation: 2026-11-04

## Verified results

- Baseline original suite: 6 passed
- Expanded suite before Update: 40 passed
- Final local suite: 45 passed
- Independent local rerun: 45 passed, 1 warning
- Tested module: app/main.py
- Line and branch coverage reported: 100%
- Measured statements: 71
- Missed statements: 0
- Measured branches: 8
- Partial branches: 0

## Functionality

The working copy includes Create, Read, Update and Delete operations.
Five tests were added specifically for PUT behavior, including
successful updates, missing resources, input validation and persistence.

## Evidence provenance

The laboratory retains pytest outputs, coverage JSON/XML,
source integrity manifests, and SHA-256 audit logs under evidence/G4
and evidence/G5. Those internal directories are not included in
the intended public release ZIP.

## Findings

One deprecation warning involving Starlette TestClient and HTTPX
was observed during testing.

The original upstream reference was verified unchanged.

## Independent rebuild

A new Python 3.12.10 virtual environment was created. Dependency installation and pip check passed. The 45-test suite passed with 100% measured coverage of app/main.py in that clean environment.

## Unverified items

- GitHub Actions execution
- Exact future dependency resolution (dependencies are not fully locked)
- Docker and PostgreSQL integration
- Production readiness and security certification

## Conclusion

Local functional test execution and coverage met the defined
acceptance threshold. The MIT License has been added. Public release remains subject to package inspection and ZIP integrity verification.
