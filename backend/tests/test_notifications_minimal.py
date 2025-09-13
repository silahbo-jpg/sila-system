import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock

# Import the FastAPI app
from app.main import app

# Create test client
client = TestClient(app)

# Mock the notification service
@pytest.fixture
def mock_notification_service():
    with patch('app.services.notification_service.NotificationService') as mock_service:
        mock_instance = mock_service.return_value
        mock_instance.send_notification = AsyncMock(return_value={"status": "success", "notification_id": "test_123"})
        mock_instance.get_user_notifications = AsyncMock(return_value=[])
        mock_instance.mark_as_read = AsyncMock(return_value=True)
        yield mock_instance

# Test cases
class TestNotificationAPI:
    @pytest.mark.asyncio
    async def test_send_notification(self, mock_notification_service):
        """Test sending a notification"""
        response = client.post(
            "/api/notifications/send",
            json={
                "user_id": 1,
                "title": "Test",
                "message": "Test message",
                "channel": "email"
            }
        )
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        mock_notification_service.send_notification.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_notifications(self, mock_notification_service):
        """Test getting postgres notifications"""
        response = client.get("/api/notifications/postgres/1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        mock_notification_service.get_user_notifications.assert_called_once_with(user_id=1)
    
    @pytest.mark.asyncio
    async def test_mark_as_read(self, mock_notification_service):
        """Test marking a notification as read"""
        response = client.post("/api/notifications/test_123/read")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        mock_notification_service.mark_as_read.assert_called_once_with(notification_id="test_123")

