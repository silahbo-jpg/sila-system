import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timezone
import sys
import os

# Add the project postgres to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import the FastAPI app
from app.main import app

# Create test client
client = TestClient(app)

# Test data
TEST_NOTIFICATION = {
    "id": "test_notification_123",
    "user_id": 1,
    "title": "Test Notification",
    "message": "This is a test notification",
    "channel": "email",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "read": False,
    "metadata": {}
}

# Mock the notification service
@pytest.fixture
def mock_notification_service():
    with patch('app.services.notification_service.NotificationService') as mock_service:
        mock_instance = mock_service.return_value
        mock_instance.send_notification = AsyncMock(return_value={
            "status": "success",
            "notification_id": "test_123"
        })
        mock_instance.get_user_notifications = AsyncMock(return_value=[TEST_NOTIFICATION])
        mock_instance.mark_as_read = AsyncMock(return_value=True)
        yield mock_instance

# Test cases
class TestNotificationAPI:
    @pytest.mark.asyncio
    async def test_send_notification(self, mock_notification_service):
        """Test sending a notification"""
        test_data = {
            "user_id": 1,
            "title": "Test",
            "message": "Test message",
            "channel": "email",
            "metadata": {}
        }
        
        response = client.post(
            "/api/notifications/send",
            json=test_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "notification_id" in data
        
        # Verify the service was called with the correct data
        mock_notification_service.send_notification.assert_called_once()
        call_args = mock_notification_service.send_notification.call_args[1]
        assert call_args["user_id"] == 1
        assert call_args["title"] == "Test"
        assert call_args["message"] == "Test message"
        assert call_args["channel"] == "email"
    
    @pytest.mark.asyncio
    async def test_get_user_notifications(self, mock_notification_service):
        """Test getting postgres notifications"""
        response = client.get("/api/notifications/postgres/1")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:  # Check if list is not empty
            assert data[0]["id"] == TEST_NOTIFICATION["id"]
        
        # Verify the service was called with the correct user_id
        mock_notification_service.get_user_notifications.assert_called_once()
        call_args = mock_notification_service.get_user_notifications.call_args[1]
        assert call_args["user_id"] == 1
        assert call_args["skip"] == 0
        assert call_args["limit"] == 100
        assert call_args["read"] is None
    
    @pytest.mark.asyncio
    async def test_mark_as_read(self, mock_notification_service):
        """Test marking a notification as read"""
        response = client.post(
            "/api/notifications/test_123/read"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Verify the service was called with the correct notification_id
        mock_notification_service.mark_as_read.assert_called_once_with(
            notification_id="test_123"
        )

if __name__ == "__main__":
    # Run tests with pytest
    import pytest
    pytest.main(["-v", "test_notifications_standalone.py"])

