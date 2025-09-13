"""
User repository for database operations.

This module provides a repository for user-related database operations,
extending the base repository with user-specific functionality.
"""
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.core.security import get_password_hash, verify_password
from app.db.repositories.base import BaseRepository
from app.db.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[UserModel, UserCreate, UserUpdate]):
    """
    Repository for user-related database operations.
    
    This class extends the base repository with user-specific functionality
    like authentication and password hashing.
    """
    
    def __init__(self):
        """Initialize the User repository."""
        super().__init__(UserModel)
    
    async def get_by_email(
        self, 
        db: AsyncSession,
        email: str,
        options: Optional[list] = None
    ) -> Optional[UserModel]:
        """
        Get a User by email.
        
        Args:
            db: Async database session
            email: The email address to search for
            options: SQLAlchemy options for eager loading
            
        Returns:
            The User if found, None otherwise
        """
        try:
            query = select(self.model).where(self.model.email == email.lower())
            
            if options:
                for option in options:
                    query = query.options(option)
            
            result = await db.execute(query)
            return result.scalars().first()
            
        except Exception as e:
            logger.error(f"Error getting User by email {email}: {str(e)}")
            raise DatabaseError("Failed to retrieve User by email") from e
    
    async def create(
        self, 
        db: AsyncSession,
        obj_in: Union[UserCreate, Dict[str, Any]],
        **kwargs
    ) -> UserModel:
        """
        Create a new User with hashed password.
        
        Args:
            db: Async database session
            obj_in: User data to create
            **kwargs: Additional attributes to set on the user
            
        Returns:
            The created User
        """
        if isinstance(obj_in, dict):
            user_data = obj_in.copy()
        else:
            user_data = obj_in.dict(exclude_unset=True)
        
        # Hash the password if provided
        if "password" in user_data and user_data["password"]:
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        
        # Ensure email is lowercase
        if "email" in user_data and user_data["email"]:
            user_data["email"] = user_data["email"].lower()
        
        # Add any additional kwargs
        if kwargs:
            user_data.update(kwargs)
        
        return await super().create(db, obj_in=user_data)
    
    async def update(
        self, 
        db: AsyncSession,
        db_obj: UserModel,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        """
        Update a User, optionally hashing the password if provided.
        
        Args:
            db: Async database session
            db_obj: The database user object to update
            obj_in: The data to update the User with
            
        Returns:
            The updated User
        """
        update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, 'dict') else obj_in
        
        # Hash the password if provided
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # Ensure email is lowercase if being updated
        if "email" in update_data and update_data["email"]:
            update_data["email"] = update_data["email"].lower()
        
        return await super().update(db, db_obj, update_data)
    
    async def authenticate(
        self, 
        db: AsyncSession,
        email: str, 
        password: str,
        options: Optional[list] = None
    ) -> Optional[UserModel]:
        """
        Authenticate a User.
        
        Args:
            db: Async database session
            email: The User's email
            password: The plain text password
            options: SQLAlchemy options for eager loading
            
        Returns:
            The authenticated User if successful, None otherwise
        """
        user = await self.get_by_email(
            db=db,
            email=email.lower(),
            options=options
        )
        
        if not user or not user.hashed_password:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
    
    async def get_multi_by_ids(
        self,
        db: AsyncSession,
        user_ids: List[Any],
        skip: int = 0,
        limit: int = 100,
        options: Optional[list] = None
    ) -> List[UserModel]:
        """
        Get multiple users by their IDs.
        
        Args:
            db: Async database session
            user_ids: List of User IDs to retrieve
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            options: SQLAlchemy options for eager loading
            
        Returns:
            A list of User instances
        """
        try:
            if not user_ids:
                return []
                
            query = select(self.model).where(self.model.id.in_(user_ids))
            
            if options:
                for option in options:
                    query = query.options(option)
                    
            query = query.offset(skip).limit(limit)
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting users by IDs: {str(e)}")
            raise DatabaseError("Failed to retrieve users by IDs") from e


# Create a global instance for easy import
user_repo = UserRepository()