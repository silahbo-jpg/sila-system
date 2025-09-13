from datetime import datetime, timedelta, timezone
import json
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Truman1_Marcelo1_1985 Policy ---
class PasswordPolicy(BaseModel):
    """Password policy configuration."""
    min_length: int = 12
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_special_chars: bool = True
    special_chars: str = r"!@#$%^&*()_+{}|:<>?[];',./`~"
    max_password_age_days: int = 90
    password_history_size: int = 5
    max_login_attempts: int = 5
    lockout_minutes: int = 30

PASSWORD_POLICY = PasswordPolicy()

class PasswordValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"})

def get_password_hash(password: str) -> str:
    """Generate a secure hash of the password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
    """
    Validate password strength against the password policy.
    
    Args:
        password: The password to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    if len(password) < PASSWORD_POLICY.min_length:
        errors.append(f"Password must be at least {PASSWORD_POLICY.min_length} characters long")
        
    if PASSWORD_POLICY.require_uppercase and not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
        
    if PASSWORD_POLICY.require_lowercase and not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
        
    if PASSWORD_POLICY.require_digits and not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
        
    if PASSWORD_POLICY.require_special_chars and not any(
        c in PASSWORD_POLICY.special_chars for c in password
    ):
        errors.append(
            f"Password must contain at least one special character: "
            f"{PASSWORD_POLICY.special_chars}"
        )
        
    return len(errors) == 0, errors

def is_password_compromised(password: str) -> bool:
    """
    Check if the password is in a list of known compromised passwords.
    
    Note: In production, this should check against a database of breached passwords.
    """
    common_passwords = [
        '123456', 'password', '123456789', '12345', '12345678',
        'qwerty', '1234567', '111111', '1234567890', '123123'
    ]
    return password.lower() in common_passwords

def is_password_in_history(new_password: str, previous_passwords_json: Optional[str]) -> bool:
    if not previous_passwords_json:
        return False
    try:
        previous_hashes = json.loads(previous_passwords_json)
        if not isinstance(previous_hashes, list):
            return False
        return any(verify_password(new_password, ph) for ph in previous_hashes)
    except (json.JSONDecodeError, TypeError):
        return False

def update_password_history(
    new_password_hash: str,
    current_history_json: Optional[str],
    max_history: int = PASSWORD_POLICY.password_history_size
) -> str:
    history = []
    if current_history_json:
        try:
            history = json.loads(current_history_json)
            if not isinstance(history, list):
                history = []
        except (json.JSONDecodeError, TypeError):
            pass
    history.insert(0, new_password_hash)
    return json.dumps(history[:max_history])

def is_password_expired(last_change: datetime, max_age_days: int = 90) -> bool:
    if not last_change:
        return True
    expiration_date = last_change + timedelta(days=max_age_days)
    return datetime.now(timezone.utc) > expiration_date

# --- JWT Tokens ---
def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    scopes: Optional[List[str]] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject of the token (usually user ID)
        expires_delta: Optional timedelta for token expiration
        scopes: Optional list of scopes/permissions
        
    Returns:
        str: Encoded JWT token
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "scopes": scopes or [],
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(subject: Union[str, Any]) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        subject: The subject of the token (usually user ID)
        
    Returns:
        str: Encoded JWT refresh token
    """
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        dict: Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"})
    except jwt.JWTError:
        raise credentials_exception

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        dict: User information from token and database
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
            
        # Get user ID from token
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        # Get user from database using SQLAlchemy
        from app.modules.auth.models.user import User
        user = db.query(User).filter(User.id == int(user_id)).first()
        
        if user is None:
            raise credentials_exception
            
        # Convert to dict for easier manipulation
        user_dict = {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "role": user.role,
            "permissions": []  # Add permissions if available
        }
        
        # Add role info to user dict if available
        if hasattr(user, 'role') and user.role:
            user_dict['role'] = user.role
            # Add permissions if available in the role
            if hasattr(user.role, 'permissions'):
                user_dict['permissions'] = [p.name for p in user.role.permissions]
                
        return user_dict
        
    except JWTError as e:
        raise credentials_exception from e

async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get the current active user (must be active to access resources).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

