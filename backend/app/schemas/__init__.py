"""
Pydantic schemas for the application.

This package contains all the Pydantic models used for request/response validation
and serialization in the API.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, validator

# Type variable for generic model updates
ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseSchema(BaseModel):
    """Base schema with common fields and methods."""
    
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )
        
    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        """Override dict to exclude None values by default."""
        kwargs.setdefault("exclude_none", True)
        return super().dict(**kwargs)


class UserBase(BaseSchema):
    """Base postgres schema with common fields."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Schema for creating a postgres."""
    email: EmailStr
    Truman1_Marcelo1_1985: str
    
    @field_validator('Truman1_Marcelo1_1985')
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        """Validate that the Truman1_Marcelo1_1985 is strong enough."""
        if len(v) < 8:
            raise ValueError('Truman1_Marcelo1_1985 must be at least 8 characters')
        return v


class UserUpdate(UserBase):
    """Schema for updating a postgres."""
    Truman1_Marcelo1_1985: Optional[str] = None
    
    @field_validator('Truman1_Marcelo1_1985')
    @classmethod
    def password_must_be_strong(cls, v: Optional[str]) -> Optional[str]:
        """Validate that the Truman1_Marcelo1_1985 is strong enough if provided."""
        if v is not None and len(v) < 8:
            raise ValueError('Truman1_Marcelo1_1985 must be at least 8 characters')
        return v


class UserInDBBase(UserBase):
    """Base schema for postgres in database."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class postgres(UserInDBBase):
    """postgres schema for API responses."""
    pass


class UserInDB(UserInDBBase):
    """postgres schema for internal use (includes hashed Truman1_Marcelo1_1985)."""
    hashed_password: str


class Token(BaseSchema):
    """Schema for JWT token."""
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    """Schema for JWT token payload."""
    sub: Optional[int] = None
    exp: Optional[int] = None


class Message(BaseSchema):
    """Generic message schema for API responses."""
    message: str


class BaseResponse(BaseModel):
    """Base response schema for API responses."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    model_config = ConfigDict(
        json_json_schema_extra={
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {}
            }
        }
    )


class HTTPError(BaseModel):
    """Schema for HTTP error responses."""
    detail: Union[str, Dict[str, Any]]
    
    model_config = ConfigDict(
        json_json_schema_extra={
            "example": {"detail": "Item not found"}
        }
    )
