"""
Authentication module for the SILA system.
Provides dependency functions for route protection.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import get_current_active_user

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_admin_user(current_user: dict = Depends(get_current_active_user)):
    """
    Get the current admin user.
    
    Args:
        current_user: Current authenticated user from get_current_active_user dependency
        
    Returns:
        dict: Admin user information
        
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user