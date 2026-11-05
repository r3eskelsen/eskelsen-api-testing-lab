"""Synthetic isolated tests for PUT /items/{item_id}."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import Base, app, get_db


@pytest.fixture
def update_client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)

    def override_get_db():
        with factory() as session:
            yield session

    previous = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        engine.dispose()


def create_sample(client):
    result = client.post(
        "/items",
        json={"name": "Sample", "category": "QA", "quantity": 3},
    )
    assert result.status_code == 201
    return result.json()["id"]


def test_update_existing_item(update_client):
    item_id = create_sample(update_client)
    response = update_client.put(
        f"/items/{item_id}",
        json={"name": "Updated", "category": "Testing", "quantity": 8},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": item_id,
        "name": "Updated",
        "category": "Testing",
        "quantity": 8,
    }


def test_update_missing_item(update_client):
    response = update_client.put(
        "/items/999999",
        json={"name": "Missing", "category": "QA", "quantity": 1},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_rejects_negative_quantity(update_client):
    item_id = create_sample(update_client)
    response = update_client.put(
        f"/items/{item_id}",
        json={"name": "Invalid", "category": "QA", "quantity": -1},
    )
    assert response.status_code == 422
    assert update_client.get(f"/items/{item_id}").json()["quantity"] == 3


def test_update_rejects_empty_name(update_client):
    item_id = create_sample(update_client)
    response = update_client.put(
        f"/items/{item_id}",
        json={"name": "", "category": "QA", "quantity": 2},
    )
    assert response.status_code == 422


def test_update_persists_changes(update_client):
    item_id = create_sample(update_client)
    payload = {"name": "Persisted", "category": "Regression", "quantity": 12}
    response = update_client.put(f"/items/{item_id}", json=payload)
    assert response.status_code == 200

    fetched = update_client.get(f"/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == payload["name"]
    assert fetched.json()["quantity"] == payload["quantity"]
