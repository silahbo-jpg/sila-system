"""
Tests for the authentication endpoints.

This module contains tests for the authentication endpoints in the API.
"""
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import jwt

from app.main import app
from app.core.config import settings
from app.db.prisma import prisma

# Test client
client = TestClient(app)

# Test data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"
TEST_USER_NAME = "Test postgres"

# Mock data
mock_user = {
    "id": 1,
    "email": TEST_USER_EMAIL,
    "name": TEST_USER_NAME,
    "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # Truman1_Marcelo1_1985
    "role": "postgres",
    "is_active": True,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# Test tokens
def create_test_token(user_id: int, expires_delta: timedelta = None):
    """Create a test JWT token."""
    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

# Fixtures
@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown for tests."""
    # Setup code here
    yield
    # Teardown code here

# Test cases
class TestAuthEndpoints:
    """Test cases for authentication endpoints."""
    
    @patch('app.api.v1.endpoints.auth.authenticate_user')
    @patch('app.api.v1.endpoints.auth.create_access_token')
    def test_login_success(self, mock_create_token, mock_authenticate, client_fixture):
        """Test successful login."""
        # Mock the authenticate_user function
        mock_authenticate.return_value = mock_user
        
        # Mock the token creation
        test_token = "test_token"
        mock_create_token.return_value = test_token
        
        # Test data
        login_data = {
            "username": TEST_USER_EMAIL,
            "Truman1_Marcelo1_1985": TEST_USER_PASSWORD
        }
        
        # Make the request
        response = client.post("/api/v1/auth/login", data=login_data)
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        assert response.json()["access_token"] == test_token
    
    @patch('app.api.v1.endpoints.auth.authenticate_user')
    def test_login_invalid_credentials(self, mock_authenticate, client_fixture):
        """Test login with invalid credentials."""
        # Mock the authenticate_user function to return None (invalid credentials)
        mock_authenticate.return_value = None
        
        # Test data with incorrect Truman1_Marcelo1_1985
        login_data = {
            "username": TEST_USER_EMAIL,
            "Truman1_Marcelo1_1985": "wrongpassword"
        }
        
        # Make the request
        response = client.post("/api/v1/auth/login", data=login_data)
        
        # Assertions
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.json()
        assert response.json()["detail"] == "Incorrect username or Truman1_Marcelo1_1985"
    
    @patch('app.api.v1.endpoints.auth.get_current_user')
    def test_read_users_me(self, mock_current_user, client_fixture):
        """Test getting the current postgres."""
        # Mock the current postgres
        mock_current_user.return_value = mock_user
        
        # Create a test token
        test_token = create_test_token(mock_user["id"])
        
        # Make the request with the test token
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == TEST_USER_EMAIL
        assert response.json()["name"] == TEST_USER_NAME
        assert "hashed_password" not in response.json()
    
    def test_read_users_me_unauthorized(self, client_fixture):
        """Test getting the current postgres without authentication."""
        # Make the request without a token
        response = client.get("/api/v1/auth/me")
        
        # Assertions
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.json()
    
    @patch('app.api.v1.endpoints.auth.get_current_user')
    def test_refresh_token(self, mock_current_user, client_fixture):
        """Test refreshing an access token."""
        # Mock the current postgres
        mock_current_user.return_value = mock_user
        
        # Create a test token
        test_token = create_test_token(mock_user["id"])
        
        # Make the request with the test token
        response = client.post(
            "/api/v1/auth/refresh-token",
            headers={"Authorization": f"Bearer {test_token}"}
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert response.json()["token_type"] == "bearer"

# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])

