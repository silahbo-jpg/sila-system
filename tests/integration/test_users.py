"""
Integration tests for user management endpoints.

This module contains tests for user-related operations such as
retrieving, updating, and managing user accounts.
"""
import pytest
from fastapi import status
from typing import Dict, Any

class TestUsers:
    """Test cases for user management endpoints."""
    
    def test_get_current_user(self, client, auth_headers, auth_user):
        ""Test retrieving the currently authenticated user."""
        # Act
        response = client.get(
            "/api/v1/users/me",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == auth_user.email
        assert "hashed_password" not in data  # Sensitive data should be excluded
        assert "id" in data
        assert "created_at" in data
    
    def test_update_current_user(self, client, auth_headers, auth_user):
        ""Test updating the currently authenticated user."""
        # Arrange
        update_data = {
            "full_name": "Updated Name",
            "phone_number": "+5511999999999"
        }
        
        # Act
        response = client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json=update_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone_number"] == update_data["phone_number"]
    
    def test_update_password(self, client, auth_headers, auth_user):
        ""Test updating the current user's password."""
        # Arrange
        password_data = {
            "current_password": "testpassword123",
            "new_password": "new_secure_password123",
            "new_password_confirm": "new_secure_password123"
        }
        
        # Act
        response = client.put(
            "/api/v1/users/me/password",
            headers=auth_headers,
            json=password_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "Password updated successfully" in response.json()["message"]
        
        # Verify new password works
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": auth_user.email,
                "password": password_data["new_password"]
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
    
    def test_update_password_mismatch(self, client, auth_headers):
        ""Test updating password with mismatched confirmation fails."""
        # Arrange
        password_data = {
            "current_password": "testpassword123",
            "new_password": "new_secure_password123",
            "new_password_confirm": "mismatched_password"
        }
        
        # Act
        response = client.put(
            "/api/v1/users/me/password",
            headers=auth_headers,
            json=password_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "passwords do not match" in response.text.lower()
    
    def test_list_users_as_admin(self, client, admin_headers, user_factory):
        ""Test listing all users (admin only)."""
        # Arrange - create some test users
        test_users = user_factory.create_batch(3)
        
        # Act
        response = client.get(
            "/api/v1/users/",
            headers=admin_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # Should include the admin and test users
    
    def test_list_users_unauthorized(self, client, auth_headers):
        ""Test that regular users cannot list all users."""
        # Act
        response = client.get(
            "/api/v1/users/",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_user_by_id_as_admin(self, client, admin_headers, auth_user):
        ""Test retrieving a user by ID (admin only)."""
        # Act - get the current user's ID
        me_response = client.get("/api/v1/users/me", headers=admin_headers)
        user_id = me_response.json()["id"]
        
        # Get user by ID
        response = client.get(
            f"/api/v1/users/{user_id}",
            headers=admin_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == auth_user.email
    
    def test_update_user_as_admin(self, client, admin_headers, auth_user):
        ""Test updating a user as an admin."""
        # Arrange - get the user ID
        me_response = client.get("/api/v1/users/me", headers=admin_headers)
        user_id = me_response.json()["id"]
        
        update_data = {
            "is_active": False,
            "is_verified": True,
            "roles": ["user", "editor"]
        }
        
        # Act
        response = client.patch(
            f"/api/v1/users/{user_id}",
            headers=admin_headers,
            json=update_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] is False
        assert data["is_verified"] is True
        assert set(data["roles"]) == set(["user", "editor"])
    
    def test_delete_user_as_admin(self, client, admin_headers, user_factory):
        ""Test deleting a user as an admin."""
        # Arrange - create a test user
        test_user = user_factory.create()
        
        # Act
        response = client.delete(
            f"/api/v1/users/{test_user.id}",
            headers=admin_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify user no longer exists
        get_response = client.get(
            f"/api/v1/users/{test_user.id}",
            headers=admin_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
