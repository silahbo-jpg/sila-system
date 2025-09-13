import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
import os
import sys

# Add the parent directory to the path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.session import Base, engine
from app.main import app
from app.db import get_db


# Setup test database (using PostgreSQL instead of SQLite)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('TEST_DB_USER', 'test_user')}:"
    f"{os.getenv('TEST_DB_PASSWORD', 'test_password')}@"
    f"{os.getenv('TEST_DB_HOST', 'localhost')}:"
    f"{os.getenv('TEST_DB_PORT', '5432')}/"
    f"{os.getenv('TEST_DB_NAME', 'test_audit_db')}"
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


def test_log_audit_event():
    """Test logging an audit event"""
    audit_data = {
        "action": "test_action",
        "user_id": 1,
        "details": "Test audit event",
        "ip_address": "127.0.0.1"
    }
    
    response = client.post("/api/audit/log", json=audit_data)
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == audit_data["action"]
    assert data["details"] == audit_data["details"]
    assert "id" in data
    assert "created_at" in data


def test_get_audit_logs():
    """Test retrieving audit logs"""
    response = client.get("/api/audit/logs")
    assert response.status_code == 200
    logs = response.json()
    assert isinstance(logs, list)
    
    # If there are logs, verify the structure
    if logs:
        assert "id" in logs[0]
        assert "action" in logs[0]
        assert "created_at" in logs[0]