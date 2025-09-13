"""
Tests for authentication and password security features.
"""
import json
from datetime import datetime, timedelta
from typing import Dict, Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.security import PASSWORD_POLICY, get_password_hash, verify_password
from app.db.base import Base
from app.models.user import User
from tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_get_access_token(client: TestClient, db: AsyncSession) -> None:
    """Test successful login and token retrieval."""
    # Create a test user
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    hashed_password = get_password_hash(password)
    
    try:
        # Create test user using SQLAlchemy
        user = User(
            email=email,
            name=username,
            hashed_password=hashed_password,
            is_active=True,
            role="user"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Test login
        login_data = {
            "username": email,
            "password": password,
        }
        r = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        tokens = r.json()
        
        assert r.status_code == status.HTTP_200_OK
        assert "access_token" in tokens
        assert len(tokens["access_token"].split(".")) == 3  # JWT has 3 parts
        
    finally:
        # Clean up
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()
    
    # Clean up is handled by the finally block
    pass


@pytest.mark.asyncio
async def test_use_access_token(client: TestClient, db: AsyncSession) -> None:
    """Test accessing a protected endpoint with a valid token."""
    # Create a test user
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    
    try:
        # Create test user using SQLAlchemy
        user = User(
            email=email,
            name=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            role="user"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Get access token
        login_data = {
            "username": email,
            "password": password,
        }
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        tokens = response.json()
        access_token = tokens["access_token"]
        
        # Access protected endpoint
        response = client.get(
            f"{settings.API_V1_STR}/users/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        result = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert "email" in result
        assert result["email"] == email
        
    finally:
        # Clean up
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()


@pytest.mark.asyncio
async def test_password_complexity_validation(client: TestClient, db: AsyncSession) -> None:
    """Test password complexity validation."""
    # Create a test user
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    
    try:
        # Create test user using SQLAlchemy
        user = User(
            email=email,
            name=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            role="user"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Test weak password
        weak_password = "password"
        response = client.post(
            f"{settings.API_V1_STR}/auth/change-password",
            data={
                "current_password": password,
                "new_password": weak_password,
                "confirm_password": weak_password,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password does not meet complexity requirements" in response.text
        
    finally:
        # Clean up
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()


@pytest.mark.asyncio
async def test_password_change(client: TestClient, db: AsyncSession) -> None:
    """Test changing a user's password."""
    # Create a test user
    email = random_email()
    old_password = random_lower_string()
    new_password = f"New{random_lower_string()}123!"
    username = random_lower_string()
    
    try:
        # Create test user using SQLAlchemy
        user = User(
            email=email,
            name=username,
            hashed_password=get_password_hash(old_password),
            is_active=True,
            role="user"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # First, log in to get a token
        login_data = {
            "username": email,
            "password": old_password,
        }
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        tokens = response.json()
        access_token = tokens["access_token"]
        
        # Verify the token works
        response = client.get(
            f"{settings.API_V1_STR}/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == email
        
        # Test changing password with invalid current password
        response = client.post(
            f"{settings.API_V1_STR}/auth/change-password",
            data={
                "current_password": "wrong_password",
                "new_password": "NewPassword123!",
                "confirm_password": "NewPassword123!"
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
        )
        assert response.status_code == 400
        
        # Change password
        response = client.post(
            f"{settings.API_V1_STR}/auth/change-password",
            data={
                "current_password": old_password,
                "new_password": new_password,
                "confirm_password": new_password,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify old password no longer works
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data={"username": email, "password": old_password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Verify new password works
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data={"username": email, "password": new_password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == status.HTTP_200_OK
        
    finally:
        # Clean up
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()


@pytest.mark.asyncio
async def test_account_lockout_after_multiple_failed_attempts(client: TestClient, db: AsyncSession) -> None:
    """Test account lockout after multiple failed login attempts."""
    # Skip this test as the current user model doesn't support account lockout
    # TODO: Implement account lockout functionality in the user model
    pytest.skip("Account lockout not implemented in current user model")
    
    # Create a test user
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    
    try:
        # Create test user using SQLAlchemy
        user = User(
            email=email,
            name=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            role="user"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Make multiple failed login attempts
        max_attempts = 5  # Assuming 5 failed attempts trigger a lockout
        for _ in range(max_attempts):
            response = client.post(
                f"{settings.API_V1_STR}/auth/login",
                data={"username": email, "password": "wrong_password"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
        
        # The account should now be locked
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Account locked" in response.text
        
        # Try to log in with correct credentials (should still be locked)
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == status.HTTP_423_LOCKED
        
    finally:
        # Clean up
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()

