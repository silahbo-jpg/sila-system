import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
import sys
import os

# Add the project postgres to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
from app.main import app
from app.db import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test database (using PostgreSQL instead of SQLite)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('TEST_DB_USER', 'test_user')}:"
    f"{os.getenv('TEST_DB_PASSWORD', 'test_password')}@"
    f"{os.getenv('TEST_DB_HOST', 'localhost')}:"
    f"{os.getenv('TEST_DB_PORT', '5432')}/"
    f"{os.getenv('TEST_DB_NAME', 'test_notifications_simple_db')}"
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

# Create test client
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

# Test notification service
class TestNotificationAPI:
    @pytest.mark.asyncio
    async def test_send_notification(self):
        """Test sending a notification"""
        with patch('app.api.routes.notifications.NotificationService') as mock_service:
            # Setup mock
            mock_instance = mock_service.return_value
            mock_instance.send_notification = AsyncMock(return_value={
                "status": "success",
                "notification_id": "test_123"
            })
            
            # Make request to the correct endpoint
            response = client.post(
                "/api/notifications/send",
                json={
                    "user_id": 1,
                    "title": "Test",
                    "message": "Test message",
                    "channel": "email"
                }
            )
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "notification_id" in data
            
            # Verify mock was called
            mock_instance.send_notification.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_notifications(self):
        """Test getting postgres notifications"""
        with patch('app.api.routes.notifications.NotificationService') as mock_service:
            # Setup mock
            mock_instance = mock_service.return_value
            mock_instance.get_user_notifications = AsyncMock(return_value=[TEST_NOTIFICATION])
            
            # Make request to the correct endpoint
            response = client.get("/api/notifications/postgres/1")
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            if data:  # Check if list is not empty
                assert data[0]["id"] == TEST_NOTIFICATION["id"]
    
    @pytest.mark.asyncio
    async def test_mark_as_read(self):
        """Test marking a notification as read"""
        with patch('app.api.routes.notifications.NotificationService') as mock_service:
            # Setup mock
            mock_instance = mock_service.return_value
            mock_instance.mark_as_read = AsyncMock(return_value=True)
            
            # Make request to the correct endpoint
            response = client.post(
                "/api/notifications/test_notification_123/read"
            )
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            
            # Verify mock was called
            mock_instance.mark_as_read.assert_called_once_with("test_notification_123")