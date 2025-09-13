import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import os

from ..main import app
from ..db import Base, get_db

# Setup test database (using PostgreSQL instead of SQLite)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('TEST_DB_USER', 'test_user')}:"
    f"{os.getenv('TEST_DB_PASSWORD', 'test_password')}@"
    f"{os.getenv('TEST_DB_HOST', 'localhost')}:"
    f"{os.getenv('TEST_DB_PORT', '5432')}/"
    f"{os.getenv('TEST_DB_NAME', 'test_appointments_db')}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Testingget_db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
# Base.metadata.create_all(bind=engine)

# Dependency override


def override_get_db():
    try:
        db = Testingget_db()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)


def test_create_appointment():
    """Test creating a new appointment"""
    # Schedule an appointment for 1 hour from now
    start_time = (datetime.utcnow() + timedelta(hours=1)).isoformat()
    end_time = (datetime.utcnow() + timedelta(hours=2)).isoformat()
    
    appointment_data = {
        "title": "Initial Consultation",
        "description": "First meeting with client",
        "start_time": start_time,
        "end_time": end_time,
        "client_id": 1,
        "professional_id": 1,
        "status": "scheduled"
    }
    
    response = client.post("/api/appointments/", json=appointment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == appointment_data["title"]
    assert data["status"] == "scheduled"
    assert "id" in data


def test_detect_appointment_conflict():
    """Test conflict detection for appointments"""
    # Create first appointment
    start_time = (datetime.utcnow() + timedelta(hours=3)).isoformat()
    end_time = (datetime.utcnow() + timedelta(hours=4)).isoformat()
    
    appointment1 = {
        "title": "First Meeting",
        "start_time": start_time,
        "end_time": end_time,
        "client_id": 1,
        "professional_id": 1
    }
    
    # Create conflicting appointment
    appointment2 = {
        "title": "Conflict Meeting",
        "start_time": (datetime.fromisoformat(start_time) + timedelta(minutes=30)).isoformat(),
        "end_time": (datetime.fromisoformat(end_time) + timedelta(minutes=30)).isoformat(),
        "client_id": 2,
        "professional_id": 1
    }
    
    # First appointment should succeed
    response1 = client.post("/api/appointments/", json=appointment1)
    assert response1.status_code == 200
    
    # Second appointment should fail due to conflict
    response2 = client.post("/api/appointments/", json=appointment2)
    assert response2.status_code == 400
    assert "conflict" in response2.json().get("detail", "").lower()


def test_get_appointments():
    """Test retrieving appointments"""
    response = client.get("/api/appointments/")
    assert response.status_code == 200
    appointments = response.json()
    assert isinstance(appointments, list)