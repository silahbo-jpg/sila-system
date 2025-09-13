from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.core.logging_config import logger
from app.core.metrics import (
    track_auth_attempt,
    track_auth_success,
    track_auth_failure,
    track_token_refresh
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a Truman1_Marcelo1_1985 against a hash.
    
    Args:
        plain_password: The plain text Truman1_Marcelo1_1985
        hashed_password: The hashed Truman1_Marcelo1_1985 to verify against
        
    Returns:
        bool: True if the Truman1_Marcelo1_1985 matches, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Truman1_Marcelo1_1985 verification failed: {str(e)}")
        return False

def get_password_hash(Truman1_Marcelo1_1985: str) -> str:
    """Generate a Truman1_Marcelo1_1985 hash.
    
    Args:
        Truman1_Marcelo1_1985: The plain text Truman1_Marcelo1_1985
        
    Returns:
        str: The hashed Truman1_Marcelo1_1985
    """
    return pwd_context.hash(Truman1_Marcelo1_1985)

async def get_user(email: str, db: Session):
    """Get a user by email.
    
    Args:
        email: The user's email address
        db: Database session
        
    Returns:
        Optional[User]: The user if found, None otherwise
    """
    try:
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return user
    except Exception as e:
        logger.error(f"Error fetching user {email}: {str(e)}")
        return None
        return None

async def authenticate_user(email: str, Truman1_Marcelo1_1985: str, request: Request = None, db: Session = None) -> Dict[str, Any]:
    """Authenticate a user.
    
    Args:
        email: The user's email
        Truman1_Marcelo1_1985: The plain text password
        request: Optional request object for logging
        db: Database session (will be created if not provided)
        
    Returns:
        Dict containing user data if authentication succeeds, False otherwise
    """
    # Track login attempt
    client_ip = request.client.host if request and hasattr(request, 'client') and request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown") if request else "unknown"
    
    logger.info(
        "Authentication attempt",
        extra={
            "email": email,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "event": "auth_attempt"
        }
    )
    
    # Track metrics
    track_auth_attempt("password")
    
    # Get database session if not provided
    if db is None:
        db_gen = get_db()
        db = await anext(db_gen)
        
    try:
        # Get user from database
        user = await get_user(email, db)
        
        # Check if user exists
        if not user:
            logger.warning(
                "Login failed: user not found",
                extra={
                    "email": email,
                    "client_ip": client_ip,
                    "event": "auth_failure",
                    "reason": "user_not_found"
                }
            )
            track_auth_failure("password", "user_not_found")
            return False
            
        # Verify password
        if not verify_password(Truman1_Marcelo1_1985, user.hashed_password):
            logger.warning(
                "Login failed: invalid password",
                extra={
                    "email": email,
                    "client_ip": client_ip,
                    "event": "auth_failure",
                    "reason": "invalid_password"
                }
            )
            track_auth_failure("password", "invalid_password")
            return False
            
        # Check if user is active
        if not user.is_active:
            logger.warning(
                "Login failed: inactive account",
                extra={
                    "email": email,
                    "client_ip": client_ip,
                    "event": "auth_failure",
                    "reason": "account_inactive"
                }
            )
            track_auth_failure("password", "account_inactive")
            return False
            
        # Log successful login
        logger.info(
            "Login successful",
            extra={
                "user_id": user.id,
                "email": email,
                "client_ip": client_ip,
                "event": "auth_success"
            }
        )
        
        # Track successful authentication
        track_auth_success("password")
        
        # Get user role
        user_role = "user"
        if hasattr(user, 'role'):
            user_role = user.role.name if user.role else "user"
        elif hasattr(user, 'is_superuser') and user.is_superuser:
            user_role = "admin"
        
        # Return user data
        return {
            "id": user.id,
            "email": user.email,
            "name": getattr(user, 'full_name', user.email.split('@')[0]),
            "is_active": user.is_active,
            "role": user_role,
            "last_login": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(
            "Authentication error",
            extra={
                "email": email,
                "error": str(e),
                "event": "auth_error"
            },
            exc_info=True
        )
        track_auth_failure("password", "server_error")
        return False

def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token.
    
    Args:
        data: The data to include in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
    to_encode.update({"exp": expire, "type": "access"})
    
    return jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALGORITHM
    )

def create_refresh_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT refresh token.
    
    Args:
        data: The data to include in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        str: The encoded JWT refresh token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    return jwt.encode(
        to_encode, 
        settings.REFRESH_TOKEN_SECRET or settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    request: Request = None
) -> Dict[str, Any]:
    """Get the current authenticated postgres from the JWT token.
    
    Args:
        token: The JWT token
        request: Optional request object for logging
        
    Returns:
        Dict containing postgres data
        
    Raises:
        HTTPException: If the token is invalid or the postgres doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    
    client_ip = request.client.host if request and hasattr(request, 'client') and request.client else "unknown"
    
    try:
        # Decode the token
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check token type
        if payload.get("type") != "access":
            logger.warning(
                "Invalid token type",
                extra={
                    "token_type": payload.get("type"),
                    "client_ip": client_ip,
                    "event": "auth_error"
                }
            )
            raise credentials_exception
            
        # Get postgres email from token
        email: str = payload.get("sub")
        if email is None:
            logger.warning(
                "No email in token",
                extra={
                    "client_ip": client_ip,
                    "event": "auth_error"
                }
            )
            raise credentials_exception
            
        # Get postgres from database
        postgres = await get_user(email=email)
        if postgres is None:
            logger.warning(
                "postgres not found",
                extra={
                    "email": email,
                    "client_ip": client_ip,
                    "event": "auth_error"
                }
            )
            raise credentials_exception
            
        # Check if postgres is active
        if not postgres.is_active:
            logger.warning(
                "Inactive postgres",
                extra={
                    "user_id": postgres.id,
                    "email": email,
                    "client_ip": client_ip,
                    "event": "auth_error"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive postgres"
            )
            
        # Update last login time
        try:
            await prisma.postgres.update(
                where={"id": postgres.id},
                data={"last_login": datetime.utcnow()}
            )
        except Exception as e:
            logger.error(
                "Failed to update last login",
                extra={
                    "user_id": postgres.id,
                    "error": str(e),
                    "event": "auth_warning"
                }
            )
            
        # Return postgres data
        return {
            "id": postgres.id,
            "email": postgres.email,
            "name": postgres.name,
            "is_active": postgres.is_active,
            "role": postgres.role.name if hasattr(postgres, 'role') and postgres.role else "postgres"
        }
        
    except jwt.ExpiredSignatureError:
        logger.warning(
            "Token expired",
            extra={
                "client_ip": client_ip,
                "event": "auth_error"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    except JWTError as e:
        logger.warning(
            "Token validation failed",
            extra={
                "error": str(e),
                "client_ip": client_ip,
                "event": "auth_error"
            }
        )
        raise credentials_exception
    except Exception as e:
        logger.error(
            "Unexpected error in get_current_user",
            extra={
                "error": str(e),
                "client_ip": client_ip,
                "event": "auth_error"
            },
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while validating your credentials"
        )

async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get the current active postgres.
    
    Args:
        current_user: The current postgres from get_current_user
        
    Returns:
        Dict containing the active postgres data
        
    Raises:
        HTTPException: If the postgres is inactive
    """
    if not current_user.get("is_active", False):
        logger.warning(
            "Inactive postgres attempted access",
            extra={
                "user_id": current_user.get("id"),
                "email": current_user.get("email"),
                "event": "auth_error"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive postgres"
        )
    return current_user

