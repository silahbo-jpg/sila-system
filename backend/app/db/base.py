"""
Base model for SQLAlchemy models.

This module contains the base class for all database models with common functionality
like automatic table naming, timestamps, and utility methods.
"""
from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar
from uuid import UUID as UUIDType, uuid4

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session

# Type variable for generic model type
ModelType = TypeVar("ModelType", bound="Base")

class BaseMixin:
    """Mixin class that provides common functionality for all models."""
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically based on class name.
        Converts CamelCase to snake_case.
        """
        return ''.join(['_' + i.lower() if i.isupper() else i 
                      for i in cls.__name__]).lstrip('_')
    
    # Common columns for all models
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns  # type: ignore
        }
    
    @classmethod
    def get_by_id(
        cls: Type[ModelType], 
        db: Session, 
        id: int
    ) -> Optional[ModelType]:
        """Get a model instance by ID."""
        return db.query(cls).filter(cls.id == id).first()
    
    def update(self, db: Session, **kwargs) -> None:
        """Update model instance with given attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.add(self)
        db.commit()
        db.refresh(self)

# Create declarative base with our mixin
@as_declarative()
class Base(BaseMixin):
    """Base class for all SQLAlchemy models."""
    __name__: str
    
    # This allows proper type hints for columns
    id: int
    created_at: datetime
    updated_at: datetime
    
    # This is needed for proper type checking with mypy
    __table__: Any
