"""Tests for internal module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def internal_data():
    return {}


def test_create_internal(client: TestClient, db: Session, internal_data: dict):
    """Test creating a new internal."""
    response = client.post("/internals/", json=internal_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
