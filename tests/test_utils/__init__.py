"""Test utilities for the SILA System."""
from typing import Dict, Any, Optional
import json
from fastapi.testclient import TestClient


def assert_response(
    response,
    status_code: int = 200,
    expected_data: Optional[Dict[str, Any]] = None,
    expected_keys: Optional[list] = None,
):
    """Assert common response patterns.
    
    Args:
        response: The response object from TestClient
        status_code: Expected HTTP status code
        expected_data: Expected data in response
        expected_keys: List of keys that should be in the response
    """
    assert response.status_code == status_code, (
        f"Expected status code {status_code}, got {response.status_code}. "
        f"Response: {response.text}"
    )
    
    if expected_data is not None:
        response_data = response.json()
        assert response_data == expected_data, (
            f"Response data does not match expected. "
            f"Expected: {expected_data}, Got: {response_data}"
        )
    
    if expected_keys is not None:
        response_data = response.json()
        for key in expected_keys:
            assert key in response_data, f"Expected key '{key}' not in response"


def create_test_user(
    client: TestClient, 
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "testpassword123"
) -> Dict[str, str]:
    """Helper to create a test user and return auth tokens."""
    # Register user
    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "password_confirm": password,
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201, f"Failed to create test user: {response.text}"
    
    # Login to get tokens
    login_data = {
        "username": username,
        "password": password,
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200, f"Failed to login test user: {response.text}"
    
    tokens = response.json()
    return {
        "access_token": tokens["access_token"],
        "token_type": tokens["token_type"],
        "headers": {"Authorization": f"Bearer {tokens['access_token']}"}
    }
