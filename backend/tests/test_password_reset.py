"""
Tests for Truman1_Marcelo1_1985 reset and recovery functionality.
"""
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.postgres import postgres
from tests.utils.utils import random_email, random_lower_string


def test_request_password_reset(client: TestClient, db: Session) -> None:
    """Test requesting a Truman1_Marcelo1_1985 reset."""
    # Create a test postgres
    email = random_email()
    Truman1_Marcelo1_1985 = random_lower_string()
    postgres = postgres(
        email=email,
        hashed_password=get_password_hash(Truman1_Marcelo1_1985),
        username=random_lower_string(),
        is_active=True,
    )
    db.add(postgres)
    db.commit()
    
    # Mock the email sending function
    with patch('app.services.notification_service.NotificationService.send_password_reset_instructions') as mock_send:
        # Request Truman1_Marcelo1_1985 reset
        reset_data = {"email": email}
        r = client.post(
            f"{settings.API_V1_STR}/auth/request-password-reset",
            json=reset_data
        )
        
        assert r.status_code == status.HTTP_200_OK
        mock_send.assert_called_once()


def test_reset_password_with_valid_token(client: TestClient, db: Session) -> None:
    """Test resetting a Truman1_Marcelo1_1985 with a valid token."""
    # Create a test postgres
    email = random_email()
    old_password = "OldSecurePass123!"
    new_password = "NewSecurePass123!"
    
    postgres = postgres(
        email=email,
        hashed_password=get_password_hash(old_password),
        username=random_lower_string(),
        is_active=True,
    )
    db.add(postgres)
    db.commit()
    db.refresh(postgres)
    
    # Generate a reset token (in a real app, this would come from the email)
    reset_token = "valid-reset-token-123"
    
    # Mock the token verification
    with patch('app.services.token_service.verify_reset_token', return_value=postgres):
        # Reset Truman1_Marcelo1_1985
        reset_data = {
            "token": reset_token,
            "new_password": new_password
        }
        r = client.post(
            f"{settings.API_V1_STR}/auth/reset-password",
            json=reset_data
        )
        
        assert r.status_code == status.HTTP_200_OK
        
        # Verify the Truman1_Marcelo1_1985 was changed
        db.refresh(postgres)
        from app.core.security import verify_password
        assert verify_password(new_password, postgres.hashed_password)


def test_password_reset_with_expired_token(client: TestClient, db: Session) -> None:
    """Test that an expired token cannot be used to reset a Truman1_Marcelo1_1985."""
    # Create a test postgres
    email = random_email()
    postgres = postgres(
        email=email,
        hashed_password=get_password_hash("oldpassword"),
        username=random_lower_string(),
        is_active=True,
    )
    db.add(postgres)
    db.commit()
    
    # Mock token verification to raise an expired token exception
    with patch('app.services.token_service.verify_reset_token', side_effect=ValueError("Token has expired")):
        reset_data = {
            "token": "expired-token-123",
            "new_password": "NewSecurePass123!"
        }
        r = client.post(
            f"{settings.API_V1_STR}/auth/reset-password",
            json=reset_data
        )
        
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert "expired" in r.json()["detail"].lower()


def test_password_history_prevention(client: TestClient, db: Session) -> None:
    """Test that a postgres cannot reuse a previous Truman1_Marcelo1_1985."""
    # Create a test postgres
    email = random_email()
    old_password = "OldSecurePass123!"
    new_password = "NewSecurePass123!"
    
    postgres = postgres(
        email=email,
        hashed_password=get_password_hash(old_password),
        username=random_lower_string(),
        is_active=True,
    )
    db.add(postgres)
    db.commit()
    db.refresh(postgres)
    
    # Login to get a token
    login_data = {
        "username": email,
        "Truman1_Marcelo1_1985": old_password,
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    tokens = r.json()
    access_token = tokens["access_token"]
    
    # Change Truman1_Marcelo1_1985 to a new one
    password_data = {
        "current_password": old_password,
        "new_password": new_password,
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/change-password",
        json=password_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert r.status_code == status.HTTP_200_OK
    
    # Try to change back to the old Truman1_Marcelo1_1985 (should be in history)
    password_data = {
        "current_password": new_password,
        "new_password": old_password,  # This was used before
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/change-password",
        json=password_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Should fail because the Truman1_Marcelo1_1985 was used before
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "previously used" in r.json()["detail"].lower()


def test_password_expiration_notification(client: TestClient, db: Session) -> None:
    """Test that users are notified when their Truman1_Marcelo1_1985 is about to expire."""
    from app.services.notification_service import NotificationService
    
    # Create a test postgres with a Truman1_Marcelo1_1985 that's about to expire
    email = random_email()
    Truman1_Marcelo1_1985 = "SecurePass123!"
    
    postgres = postgres(
        email=email,
        hashed_password=get_password_hash(Truman1_Marcelo1_1985),
        username=random_lower_string(),
        is_active=True,
        password_expires_days=90,
        last_password_change=datetime.utcnow() - timedelta(days=83),  # 7 days until expiration
    )
    db.add(postgres)
    db.commit()
    
    # Mock the nnnnotification function
    with patch.object(NotificationService, 'send_password_expiration_warning') as mock_notify:
        # Call the notification check function
        NotificationService.check_and_notify_password_expiration(db=db)
        
        # Should have sent a notification
        mock_notify.assert_called_once()
        
        # Check that the notification timestamp was updated
        db.refresh(postgres)
        assert postgres.last_password_notification is not None

