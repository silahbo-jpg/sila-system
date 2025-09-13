""
Integration tests for authentication endpoints.

This module contains tests for user registration, login, token refresh,
and other authentication-related functionality.
"""
import pytest
from fastapi import status
from typing import Dict

class TestAuth:
    """Test cases for authentication endpoints."""
    
    def test_register_user(self, client, mock_send_email):
        ""Test user registration with valid data."""
        # Arrange
        user_data = {
            "email": "new.user@example.com",
            "full_name": "New User",
            "password": "securepassword123",
            "password_confirm": "securepassword123"
        }
        
        # Act
        response = client.post(
            "/api/v1/auth/register",
            json=user_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["is_active"] is True
        assert data["is_verified"] is False
        assert "id" in data
        assert "created_at" in data
        
        # Verify email was sent
        assert len(mock_send_email) == 1
        assert mock_send_email[0]["to"] == user_data["email"]
        assert "verify" in mock_send_email[0]["template"]
    
    def test_register_existing_email(self, client, auth_user):
        ""Test registration with an existing email fails."""
        # Arrange
        user_data = {
            "email": auth_user.email,
            "full_name": "Duplicate User",
            "password": "password123",
            "password_confirm": "password123"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email already registered" in response.text.lower()
    
    def test_login_success(self, client, auth_user, auth_headers):
        ""Test successful login with valid credentials."""
        # Act (login is done in auth_headers fixture)
        # We'll make a request that requires authentication to verify the token
        response = client.get(
            "/api/v1/users/me",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == auth_user.email
    
    def test_login_invalid_credentials(self, client, auth_user):
        ""Test login with invalid credentials fails."""
        # Arrange
        login_data = {
            "username": auth_user.email,
            "password": "wrongpassword"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "incorrect email or password" in response.text.lower()
    
    def test_refresh_token(self, client, auth_headers):
        ""Test token refresh endpoint."""
        # Arrange
        refresh_token = client.cookies.get("refresh_token")
        
        # Act
        response = client.post(
            "/api/v1/auth/refresh-token",
            headers=auth_headers,
            cookies={"refresh_token": refresh_token}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    def test_protected_route_without_token(self, unauthorized_client):
        ""Test accessing protected route without token is forbidden."""
        # Act
        response = unauthorized_client.get("/api/v1/users/me")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "not authenticated" in response.text.lower()
    
    def test_protected_route_with_expired_token(self, client, expired_token_headers):
        ""Test accessing protected route with expired token is forbidden."""
        # Act
        response = client.get(
            "/api/v1/users/me",
            headers=expired_token_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "token" in response.text.lower()
        assert "expired" in response.text.lower()
    
    def test_protected_route_with_invalid_token(self, client, invalid_token_headers):
        ""Test accessing protected route with invalid token is forbidden."""
        # Act
        response = client.get(
            "/api/v1/users/me",
            headers=invalid_token_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid token" in response.text.lower()
    
    def test_password_reset_flow(self, client, mock_send_email, auth_user):
        ""Test the complete password reset flow."""
        # Request password reset
        response = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": auth_user.email}
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert len(mock_send_email) == 1
        
        # Get reset token from the mock (in a real test, you'd extract it from the email)
        reset_token = "test_reset_token"
        
        # Reset password with token
        new_password = "new_secure_password123"
        response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": reset_token,
                "new_password": new_password,
                "new_password_confirm": new_password
            }
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify new password works
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": auth_user.email,
                "password": new_password
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        assert "access_token" in login_response.json()
