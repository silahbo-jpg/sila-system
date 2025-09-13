"""Tests for social module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def social_data():
    return {}


def test_create_social(client: TestClient, db: Session, social_data: dict):
    """Test creating a new social."""
    response = client.post("/socials/", json=social_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
