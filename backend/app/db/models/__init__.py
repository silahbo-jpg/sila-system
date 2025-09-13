"""Database models package.

This package contains all SQLAlchemy models for the application.
"""
from app.db.base import Base
from .user import User, Role, Permission, role_permissions, user_permissions

# Import all models here to ensure they are registered with SQLAlchemy
__all__ = [
    'Base',
    'User',
    'Role',
    'Permission',
    'role_permissions',
    'user_permissions',
]
