"""Isolated, synthetic FastAPI test fixtures. Network and persistent DBs are forbidden."""
import os
from contextlib import contextmanager

assert os.environ.get("DATABASE_URL") == "sqlite:///:memory:", (
    "G3 refuses to import the application unless DATABASE_URL=sqlite:///:memory:"
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.main import Base, app, get_db

@contextmanager
def make_client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)

    def override_db():
        with Session(test_engine) as session:
            yield session

    previous = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = override_db
    try:
        with TestClient(app) as api:
            yield api
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        test_engine.dispose()

@pytest.fixture
def isolated_client_factory():
    return make_client

@pytest.fixture
def api_client(isolated_client_factory):
    with isolated_client_factory() as api:
        yield api
