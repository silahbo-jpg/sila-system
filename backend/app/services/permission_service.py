"""
Permission service for handling user permissions and role-based access control.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
import logging

from app.db.models.user import User as UserModel
from app.db.models.role import Role
from app.db.session import get_db
from app.schemas.user import UserInDB
from app.core.permissions import Permissions

logger = logging.getLogger("permissions")

class PermissionService:
    """Service for handling permission-related operations."""
    
    @staticmethod
    async def get_user_permissions(db: AsyncSession, user: UserModel) -> List[str]:
        """
        Get all permissions for a user, including those from their role.
        
        Args:
            db: Async database session
            user: User model instance
            
        Returns:
            List of permission strings (e.g., ["users:read", "users:write"])
        """
        try:
            from sqlalchemy.orm import selectinload
            from sqlalchemy.future import select
            
            # Start with an empty list of permissions
            permissions = []
            
            # Query the user with their role and permissions
            query = (
                select(UserModel)
                .options(
                    selectinload(UserModel.role).selectinload(Role.permissions),
                    selectinload(UserModel.permissions)
                )
                .where(UserModel.id == user.id)
            )
            
            result = await db.execute(query)
            db_user = result.scalars().first()
            
            if not db_user:
                logger.warning(f"User {user.id} not found when fetching permissions")
                return []
            
            # Add permissions from user's role if exists
            if db_user.role and db_user.role.permissions:
                permissions.extend([p.name for p in db_user.role.permissions])
            
            # Add any direct permissions from the user
            if db_user.permissions:
                permissions.extend([p.name for p in db_user.permissions])
            
            # Add user permissions if user is superuser
            if db_user.is_superuser:
                permissions.append("user")
            
            return list(set(permissions))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error getting user permissions: {e}", exc_info=True)
            return []
    
    @staticmethod
    def has_permission(user_permissions: List[str], required_permission: str) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            user_permissions: List of the user's permissions
            required_permission: The permission to check (e.g., "users:read")
            
        Returns:
            bool: True if the user has the permission, False otherwise
        """
        if not user_permissions:
            return False
            
        # Superusers have all permissions
        if "user" in user_permissions:
            return True
            
        # Check for exact match or wildcard permission
        permission_parts = required_permission.split(':')
        if len(permission_parts) < 2:
            return required_permission in user_permissions
            
        return (
            required_permission in user_permissions or
            f"{permission_parts[0]}:*" in user_permissions
        )
    
    @classmethod
    async def check_permission(
        cls, 
        db: AsyncSession, 
        user: UserModel, 
        required_permission: str
    ) -> bool:
        """
        Check if a user has a specific permission by fetching their permissions.
        
        Args:
            db: Async database session
            user: User model instance
            required_permission: The permission to check
            
        Returns:
            bool: True if the user has the permission, False otherwise
        """
        permissions = await cls.get_user_permissions(db, user)
        return cls.has_permission(permissions, required_permission)
    
    @staticmethod
    def has_any_permission(user_permissions: List[str], *required_permissions: str) -> bool:
        """
        Check if a user has any of the specified permissions.
        
        Args:
            user_permissions: List of the user's permissions
            *required_permissions: One or more permissions to check
            
        Returns:
            bool: True if the user has at least one of the required permissions
        """
        if not user_permissions:
            return False
            
        # Superusers have all permissions
        if "user" in user_permissions:
            return True
            
        return any(
            PermissionService.has_permission(user_permissions, perm)
            for perm in required_permissions
        )
    
    @classmethod
    async def check_any_permission(
        cls,
        db: AsyncSession,
        user: UserModel,
        *required_permissions: str
    ) -> bool:
        """
        Check if a user has any of the specified permissions by fetching their permissions.
        
        Args:
            db: Async database session
            user: User model instance
            *required_permissions: One or more permissions to check
            
        Returns:
            bool: True if the user has at least one of the required permissions
        """
        permissions = await cls.get_user_permissions(db, user)
        return cls.has_any_permission(permissions, *required_permissions)
    
    @staticmethod
    def has_all_permissions(user_permissions: List[str], *required_permissions: str) -> bool:
        """
        Check if a user has all of the specified permissions.
        
        Args:
            user_permissions: List of the user's permissions
            *required_permissions: One or more permissions to check
            
        Returns:
            bool: True if the user has all of the required permissions
        """
        if not user_permissions:
            return False
            
        # Superusers have all permissions
        if "user" in user_permissions:
            return True
            
        return all(
            PermissionService.has_permission(user_permissions, perm)
            for perm in required_permissions
        )
    
    @classmethod
    async def check_all_permissions(
        cls,
        db: AsyncSession,
        user: UserModel,
        *required_permissions: str
    ) -> bool:
        """
        Check if a user has all of the specified permissions by fetching their permissions.
        
        Args:
            db: Async database session
            user: User model instance
            *required_permissions: One or more permissions to check
            
        Returns:
            bool: True if the user has all of the required permissions
        """
        permissions = await cls.get_user_permissions(db, user)
        return cls.has_all_permissions(permissions, *required_permissions)