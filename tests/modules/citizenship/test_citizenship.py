"""Tests for citizenship module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def citizenship_data():
    return {}


def test_create_citizenship(client: TestClient, db: Session, citizenship_data: dict):
    """Test creating a new citizenship."""
    response = client.post("/citizenships/", json=citizenship_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
