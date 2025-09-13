"""Tests for justice module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def justice_data():
    return {}


def test_create_justice(client: TestClient, db: Session, justice_data: dict):
    """Test creating a new justice."""
    response = client.post("/justices/", json=justice_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
