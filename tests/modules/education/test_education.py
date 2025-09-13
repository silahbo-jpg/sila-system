"""Tests for education module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def education_data():
    return {}


def test_create_education(client: TestClient, db: Session, education_data: dict):
    """Test creating a new education."""
    response = client.post("/educations/", json=education_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
