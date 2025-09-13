"""
Base repository for database operations.

This module provides a base repository class with common CRUD operations
that can be extended by model-specific repositories.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Type, cast

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel as PydanticBaseModel

from app.core.exceptions import DatabaseError, ResourceNotFound

# Type variables
T = TypeVar('T')
ModelType = TypeVar('ModelType', bound=Any)
CreateSchemaType = TypeVar('CreateSchemaType', bound=PydanticBaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=PydanticBaseModel)

# Configure logger
logger = logging.getLogger(__name__)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """
    Base repository class with common CRUD operations.
    
    This class provides a standard interface for database operations
    that can be reused across different model repositories.
    
    Attributes:
        model: The SQLAlchemy model class
    """
    
    def __init__(self, model: Type[ModelType]):
        """Initialize the repository with a SQLAlchemy model."""
        self.model = model
    
    async def get_by_id(
        self, 
        db: AsyncSession, 
        id: Any,
        options: Optional[list] = None
    ) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            db: Async database session
            id: The ID of the record to retrieve
            options: SQLAlchemy options for eager loading
            
        Returns:
            The model instance if found, None otherwise
        """
        try:
            query = select(self.model).where(self.model.id == id)
            
            if options:
                for option in options:
                    query = query.options(option)
                    
            result = await db.execute(query)
            return result.scalars().first()
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model.__name__} by ID {id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve {self.model.__name__} by ID") from e
    
    async def get_or_404(
        self,
        db: AsyncSession,
        id: Any,
        options: Optional[list] = None
    ) -> ModelType:
        """
        Get a single record by ID or raise a 404 error if not found.
        
        Args:
            db: Async database session
            id: The ID of the record to retrieve
            options: SQLAlchemy options for eager loading
            
        Returns:
            The model instance if found
            
        Raises:
            ResourceNotFound: If the record is not found
        """
        obj = await self.get_by_id(db, id, options=options)
        if not obj:
            raise ResourceNotFound(resource=self.model.__name__, id=id)
        return obj
    
    async def get_many(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[list] = None,
        order_by: Optional[list] = None,
        options: Optional[list] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination and filtering.
        
        Args:
            db: Async database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            filters: List of filter conditions
            order_by: List of columns to order by
            options: SQLAlchemy options for eager loading
            
        Returns:
            A list of model instances
        """
        try:
            query = select(self.model)
            
            if filters:
                for condition in filters:
                    query = query.where(condition)
                    
            if order_by:
                query = query.order_by(*order_by)
                
            if options:
                for option in options:
                    query = query.options(option)
                    
            query = query.offset(skip).limit(limit)
            
            result = await db.execute(query)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model.__name__} list: {str(e)}")
            raise DatabaseError(f"Failed to retrieve {self.model.__name__} list") from e
    
    async def create(
        self, 
        db: AsyncSession,
        obj_in: CreateSchemaType,
        **kwargs
    ) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: Async database session
            obj_in: The data to create the record with
            **kwargs: Additional attributes to set on the model
            
        Returns:
            The created model instance
        """
        try:
            obj_data = obj_in.dict(exclude_unset=True)
            if kwargs:
                obj_data.update(kwargs)
                
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
            
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise DatabaseError(f"Failed to create {self.model.__name__}") from e
    
    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record.
        
        Args:
            db: Async database session
            db_obj: The database object to update
            obj_in: The data to update the record with
            
        Returns:
            The updated model instance
        """
        try:
            update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, 'dict') else obj_in
            
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
                    
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
            
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            raise DatabaseError(f"Failed to update {self.model.__name__}") from e
    
    async def delete(
        self, 
        db: AsyncSession,
        id: Any
    ) -> bool:
        """
        Delete a record by ID.
        
        Args:
            db: Async database session
            id: The ID of the record to delete
            
        Returns:
            True if the record was deleted, False otherwise
        """
        try:
            result = await db.execute(
                delete(self.model).where(self.model.id == id)
            )
            await db.commit()
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error deleting {self.model.__name__} {id}: {str(e)}")
            raise DatabaseError(f"Failed to delete {self.model.__name__}") from e
    
    async def count(
        self,
        db: AsyncSession,
        filters: Optional[list] = None
    ) -> int:
        """
        Count records matching the given conditions.
        
        Args:
            db: Async database session
            filters: List of filter conditions
            
        Returns:
            The number of matching records
        """
        try:
            query = select(self.model)
            
            if filters:
                for condition in filters:
                    query = query.where(condition)
                    
            result = await db.execute(select([func.count()]).select_from(query.subquery()))
            return result.scalar_one()
            
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model.__name__}: {str(e)}")
            raise DatabaseError(f"Failed to count {self.model.__name__}") from e
    
    async def exists(
        self,
        db: AsyncSession,
        **filters: Any
    ) -> bool:
        """
        Check if a record exists matching the given conditions.
        
        Args:
            db: Async database session
            **filters: Filter conditions as keyword arguments
            
        Returns:
            True if a matching record exists, False otherwise
        """
        try:
            query = select(self.model)
            
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
                    
            result = await db.execute(query.limit(1))
            return result.scalars().first() is not None
            
        except SQLAlchemyError as e:
            logger.error(f"Error checking if {self.model.__name__} exists: {str(e)}")
            raise DatabaseError(f"Failed to check if {self.model.__name__} exists") from e
