import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys
import os

# Add the project postgres to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.db import Base, get_db
from app.services.notification_service import NotificationService, notification_service

# Setup test database (using PostgreSQL instead of SQLite)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('TEST_DB_USER', 'test_user')}:"
    f"{os.getenv('TEST_DB_PASSWORD', 'test_password')}@"
    f"{os.getenv('TEST_DB_HOST', 'localhost')}:"
    f"{os.getenv('TEST_DB_PORT', '5432')}/"
    f"{os.getenv('TEST_DB_NAME', 'test_notifications_db')}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test data
TEST_NOTIFICATION = {
    "id": "test_notification_123",
    "user_id": 1,
    "title": "Test Notification",
    "message": "This is a test notification",
    "channel": "email",
    "created_at": datetime.utcnow().isoformat(),
    "read": False
}

@pytest.fixture
def mock_notification_service():
    with patch('app.services.notification_service.NotificationService') as mock:
        yield mock

# Test NotificationService
class TestNotificationService:
    @pytest.mark.asyncio
    async def test_send_notification_success(self):
        """Test sending a notification successfully"""
        service = NotificationService()
        service._send_email = AsyncMock(return_value=True)
        
        result = await service.send_notification(
            user_id=1,
            title="Test",
            message="Test message",
            channel="email"
        )
        
        assert result["status"] == "success"
        assert "notification_id" in result

# Test API Endpoints
class TestNotificationEndpoints:
    @pytest.mark.asyncio
    async def test_send_notification(self, mock_notification_service):
        """Test sending a notification via API"""
        mock_service = mock_notification_service.return_value
        mock_service.send_notification = AsyncMock(return_value={
            "status": "success",
            "notification_id": "test_123",
            "channel": "email",
            "sent_at": datetime.utcnow().isoformat()
        })
        
        response = client.post(
            "/notifications/send",
            json={
                "user_id": 1,
                "title": "Test",
                "message": "Test message",
                "channel": "email"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "notification_id" in data

    @pytest.mark.asyncio
    async def test_get_user_notifications(self, mock_notification_service):
        """Test retrieving postgres notifications"""
        mock_service = mock_notification_service.return_value
        mock_service.get_user_notifications = AsyncMock(return_value=[TEST_NOTIFICATION])
        
        response = client.get("/notifications/postgres/1")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["id"] == TEST_NOTIFICATION["id"]

    @pytest.mark.asyncio
    async def test_mark_as_read(self, mock_notification_service):
        """Test marking a notification as read"""
        mock_service = mock_notification_service.return_value
        mock_service.mark_as_read = AsyncMock(return_value=True)
        
        response = client.post(
            "/notifications/test_notification_123/mark-read"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Notification marked as read"

    @pytest.mark.asyncio
    async def test_get_notification_stats(self, mock_notification_service):
        """Test getting notification statistics"""
        mock_service = mock_notification_service.return_value
        mock_service.get_user_notifications = AsyncMock(return_value=[
            {**TEST_NOTIFICATION, "read": True},
            {**TEST_NOTIFICATION, "read": False, "id": "test_2"}
        ])
        
        response = client.get("/notifications/stats/postgres/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert data["read"] == 1
        assert data["unread"] == 1
        assert "channels" in data