"""Tests for appointments module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def appointments_data():
    return {}


def test_create_appointments(client: TestClient, db: Session, appointments_data: dict):
    """Test creating a new appointments."""
    response = client.post("/appointmentss/", json=appointments_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
