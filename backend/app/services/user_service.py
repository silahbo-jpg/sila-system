"""
User service for handling user-related operations including authentication and password management.
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB


class UserService:
    """Service for user-related operations."""

    @staticmethod
    async def get(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email."""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user with hashed password."""
        # Check if user with email already exists
        existing_user = await UserService.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = get_password_hash(user_in.password)
        
        # Create user object
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            is_active=user_in.is_active if user_in.is_active is not None else True,
            is_superuser=user_in.is_superuser if user_in.is_superuser is not None else False,
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user

    @staticmethod
    async def authenticate(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user by email and password.
        
        Args:
            db: Database session
            email: User's email
            password: Plain text password
            
        Returns:
            User object if authentication is successful, None otherwise
        """
        user = await UserService.get_by_email(db, email=email)
        if not user:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        # Update last login
        user.last_login = datetime.utcnow()
        db.add(user)
        await db.commit()
        
        return user

    @staticmethod
    async def request_password_reset(db: AsyncSession, email: str) -> bool:
        """
        Request a password reset for a user.
        
        Args:
            db: Database session
            email: User's email
            
        Returns:
            bool: True if reset email was sent, False otherwise
        """
        user = await UserService.get_by_email(db, email=email)
        if not user:
            return False
            
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        
        # Update user with reset token
        user.reset_token = reset_token
        user.reset_token_expires = reset_token_expires
        
        db.add(user)
        await db.commit()
        
        # In a real application, you would send an email with the reset link
        # For now, we'll just log it
        print(f"Password reset link: /reset-password?token={reset_token}")
        
        return True

    @staticmethod
    async def change_password(
        db: AsyncSession,
        user: User,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change a user's password.
        
        Args:
            db: Database session
            user: User object
            current_password: Current password
            new_password: New password
            
        Returns:
            bool: True if password was changed, False otherwise
        """
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            return False
            
        # Update password
        user.hashed_password = get_password_hash(new_password)
        
        db.add(user)
        await db.commit()
        
        return True

    @staticmethod
    async def reset_password(
        db: AsyncSession,
        token: str,
        new_password: str
    ) -> bool:
        """
        Reset a user's password using a reset token.
        
        Args:
            db: Database session
            token: Password reset token
            new_password: New password
            
        Returns:
            bool: True if password was reset successfully
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        result = await db.execute(
            select(User).where(
                User.reset_token == token,
                User.reset_token_expires > datetime.utcnow()
            )
        )
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )
            
        # Update password and clear reset token
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        
        db.add(user)
        await db.commit()
        
        return True

    @staticmethod
    async def update(
        db: AsyncSession,
        db_user: User,
        user_in: UserUpdate
    ) -> User:
        """
        Update user information.
        
        Args:
            db: Database session
            db_user: User to update
            user_in: New user data
            
        Returns:
            User: Updated user
            
        Raises:
            HTTPException: If email is already taken
        """
        update_data = user_in.dict(exclude_unset=True)
        
        # Check if email is being updated and if it's already taken
        if 'email' in update_data and update_data['email'] != db_user.email:
            existing_user = await UserService.get_by_email(db, email=update_data['email'])
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Update user fields
        for field, value in update_data.items():
            if field == 'password' and value is not None:
                setattr(db_user, 'hashed_password', get_password_hash(value))
            elif field != 'password' and hasattr(db_user, field):
                setattr(db_user, field, value)
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user