"""
User management endpoints.
"""
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_current_active_superuser
from app.db.session import get_db
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.db.models.user import User as UserModel

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve users with pagination (admin only).
    """
    users = await UserService.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
    current_user: UserModel = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new user (admin only).
    """
    user = await UserService.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    
    user = await UserService.create(db, obj_in=user_in)
    return user


@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = await UserService.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: UUID,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await UserService.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    
    # Only allow superusers to access other user's data
    if not current_user.is_superuser and (user.id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: UUID,
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a user (admin only).
    """
    user = await UserService.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    
    user = await UserService.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: UUID,
    current_user: UserModel = Depends(get_current_active_superuser),
) -> Any:
    """
    Delete a user (admin only).
    """
    user = await UserService.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist in the system",
        )
    
    # Prevent users from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users are not allowed to delete themselves",
        )
    
    user = await UserService.remove(db, id=user_id)
    return user
