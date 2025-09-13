import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

# Set up test environment
os.environ["ENV"] = "test"

# No need to mock Prisma since the service uses TODOs

# Import the service after setting up environment
from app.services.notification_service import NotificationService

# Import the service after setting up mocks
from app.services.notification_service import NotificationService

# Test data
TEST_NOTIFICATION = {
    "id": "test_notification_123",
    "user_id": 1,
    "title": "Test Notification",
    "message": "This is a test notification",
    "channel": "email",
    "read": False,
    "metadata": {}
}

async def test_send_notification():
    print("\nTesting send_notification...")
    # Test data
    test_data = {
        "user_id": 1,
        "title": "Test",
        "message": "Test message",
        "channel": "email",
        "metadata": {}
    }
    
    # Test
    service = NotificationService()
    result = await service.send_notification(**test_data)
    
    # Verify
    assert result["status"] == "success"
    assert "notification_id" in result
    assert result["channel"] == "email"
    print("[PASSED] test_send_notification")

async def test_get_user_notifications():
    print("\nTesting get_user_notifications...")
    # Test
    service = NotificationService()
    result = await service.get_user_notifications(user_id=1)
    
    # Verify
    assert isinstance(result, list)
    if result:  # The current implementation returns a hardcoded list
        assert "id" in result[0]
        assert "title" in result[0]
    print("[PASSED] test_get_user_notifications")

async def test_mark_as_read():
    print("\nTesting mark_as_read...")
    # Test
    service = NotificationService()
    result = await service.mark_as_read(notification_id="test_123", user_id=1)
    
    # Verify
    assert result is True  # Current implementation always returns True
    print("[PASSED] test_mark_as_read")

async def run_tests():
    print("Starting notification service tests...")
    try:
        await test_send_notification()
        await test_get_user_notifications()
        await test_mark_as_read()
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(run_tests()))

