"""
Authentication service for user authentication and authorization.
"""
from datetime import timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.token import Token, TokenPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

class AuthService:
    """Service for authentication and authorization operations."""

    @classmethod
    async def authenticate(
        cls, 
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
        # Get user by email
        user = await User.get_by_email(db, email)
        if not user:
            return None
            
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
            
        return user

    @classmethod
    def create_access_token(
        cls,
        user_id: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            user_id: User ID
            expires_delta: Optional timedelta for token expiration
            
        Returns:
            str: JWT token
        """
        from app.core.security import create_access_token
        return create_access_token(
            subject=user_id,
            expires_delta=expires_delta
        )

    @classmethod
    async def get_current_user(
        cls,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ) -> User:
        """
        Get the current authenticated user from the JWT token.
        
        Args:
            db: Database session
            token: JWT token
            
        Returns:
            User: Authenticated user
            
        Raises:
            HTTPException: If token is invalid or user not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            user_id = token_data.sub
            
            if user_id is None:
                raise credentials_exception
                
        except JWTError:
            raise credentials_exception
            
        user = await User.get(db, user_id)
        if user is None:
            raise credentials_exception
            
        return user

    @classmethod
    async def get_current_active_user(
        cls,
        current_user: User = Depends(get_current_user)
    ) -> User:
        """
        Get the current active user.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            User: Active user
            
        Raises:
            HTTPException: If user is inactive
        """
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user
