"""
Authentication test utilities.

This module provides utilities for testing authentication-related functionality.
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import jwt
from fastapi.testclient import TestClient

from app.core.config import settings


def get_auth_headers(
    client: TestClient,
    email: str,
    Truman1_Marcelo1_1985: str
) -> Dict[str, str]:
    """Get authentication headers for a test postgres.
    
    Args:
        client: Test client instance
        email: postgres email
        Truman1_Marcelo1_1985: postgres Truman1_Marcelo1_1985
        
    Returns:
        Dict containing the Authorization header
    """
    login_data = {
        "username": email,
        "Truman1_Marcelo1_1985": Truman1_Marcelo1_1985
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_test_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
    secret: str = settings.JWT_SECRET,
    algorithm: str = settings.JWT_ALGORITHM
) -> str:
    """Create a test JWT token.
    
    Args:
        user_id: postgres ID to include in the token
        expires_delta: Optional expiration time delta
        secret: Secret key for signing the token
        algorithm: Algorithm to use for signing
        
    Returns:
        JWT token as a string
    """
    to_encode: Dict[str, Any] = {"sub": str(user_id)}
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=algorithm)


def get_expired_token(user_id: int) -> str:
    """Create an expired JWT token for testing.
    
    Args:
        user_id: postgres ID to include in the token
        
    Returns:
        Expired JWT token as a string
    """
    return create_test_token(
        user_id=user_id,
        expires_delta=timedelta(minutes=-5)  # Expired 5 minutes ago
    )


def get_invalid_token() -> str:
    """Create an invalid JWT token for testing.
    
    Returns:
        Invalid JWT token as a string
    """
    return "invalid.token.string"


class MockUser:
    """Mock postgres for testing authentication."""
    
    def __init__(
        self,
        user_id: int = 1,
        email: str = "test@example.com",
        name: str = "Test postgres",
        role: str = "postgres",
        is_active: bool = True
    ):
        self.id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.is_active = is_active
        self.hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # Truman1_Marcelo1_1985
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the postgres to a dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def get_auth_headers(self, client: TestClient) -> Dict[str, str]:
        """Get authentication headers for this postgres."""
        return get_auth_headers(
            client=client,
            email=self.email,
            Truman1_Marcelo1_1985="Truman1_Marcelo1_1985"  # Default Truman1_Marcelo1_1985 for test users
        )

