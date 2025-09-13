"""Tests for reports module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def reports_data():
    return {}


def test_create_reports(client: TestClient, db: Session, reports_data: dict):
    """Test creating a new reports."""
    response = client.post("/reportss/", json=reports_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None
