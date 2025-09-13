"""
Enhanced Authentication System with JWT + 2FA for SILA

This module provides robust authentication with:
- JWT (JSON Web Tokens) for stateless authentication
- Two-Factor Authentication (2FA) support
- Multi-session management
- Security audit logging
- Rate limiting and brute force protection
- Password policy enforcement
- Device fingerprinting
"""

import jwt
import pyotp
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security
security = HTTPBearer()

class AuthenticationError(Exception):
    """Custom authentication error"""
    pass

class TwoFactorError(Exception):
    """Custom 2FA error"""
    pass

@dataclass
class AuthResult:
    """Authentication result data class"""
    success: bool
    user_id: Optional[int] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    requires_2fa: bool = False
    session_id: Optional[str] = None
    message: str = ""

@dataclass
class TokenPayload:
    """JWT token payload structure"""
    user_id: int
    session_id: str
    username: str
    role: str
    municipality: str
    exp: datetime
    iat: datetime
    device_fingerprint: Optional[str] = None

class PasswordPolicy:
    """Password policy enforcement"""
    
    MIN_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_NUMBERS = True
    REQUIRE_SPECIAL = True
    MAX_AGE_DAYS = 90
    
    @classmethod
    def validate_password(cls, password: str) -> Tuple[bool, List[str]]:
        """Validate password against policy"""
        
        errors = []
        
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters long")
            
        if cls.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
            
        if cls.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
            
        if cls.REQUIRE_NUMBERS and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
            
        if cls.REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
            
        # Check for common weak patterns
        weak_patterns = [
            r'(.)\1{2,}',  # Repeated characters
            r'123|abc|qwe|asd',  # Sequential patterns
            r'password|admin|user',  # Common words
        ]
        
        for pattern in weak_patterns:
            if re.search(pattern, password.lower()):
                errors.append("Password contains weak patterns")
                break
        
        return len(errors) == 0, errors

class TwoFactorAuth:
    """Two-Factor Authentication manager"""
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new 2FA secret"""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(user_email: str, secret: str, issuer: str = "SILA") -> str:
        """Generate QR code for 2FA setup"""
        
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 string
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
    
    @staticmethod
    def verify_token(secret: str, token: str, window: int = 1) -> bool:
        """Verify 2FA token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=window)
    
    @staticmethod
    def generate_backup_codes(count: int = 8) -> List[str]:
        """Generate backup codes for 2FA recovery"""
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()
            codes.append(f"{code[:4]}-{code[4:]}")
        return codes

class DeviceFingerprint:
    """Device fingerprinting for security"""
    
    @staticmethod
    def generate_fingerprint(request: Request) -> str:
        """Generate device fingerprint from request"""
        
        # Collect device information
        user_agent = request.headers.get("user-agent", "")
        accept_language = request.headers.get("accept-language", "")
        accept_encoding = request.headers.get("accept-encoding", "")
        client_ip = request.client.host if request.client else ""
        
        # Create fingerprint
        fingerprint_data = f"{user_agent}|{accept_language}|{accept_encoding}|{client_ip}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()
        
        return fingerprint[:16]  # Use first 16 characters

class JWTManager:
    """JWT token management"""
    
    def __init__(self):
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(minutes=30)
        self.refresh_token_expire = timedelta(days=7)
        
    def create_access_token(self, payload: TokenPayload) -> str:
        """Create JWT access token"""
        
        to_encode = {
            "sub": str(payload.user_id),
            "session_id": payload.session_id,
            "username": payload.username,
            "role": payload.role,
            "municipality": payload.municipality,
            "exp": payload.exp,
            "iat": payload.iat,
            "type": "access"
        }
        
        if payload.device_fingerprint:
            to_encode["device"] = payload.device_fingerprint
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    def create_refresh_token(self, payload: TokenPayload) -> str:
        """Create JWT refresh token"""
        
        to_encode = {
            "sub": str(payload.user_id),
            "session_id": payload.session_id,
            "exp": datetime.utcnow() + self.refresh_token_expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict:
        """Verify and decode JWT token"""
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[self.algorithm]
            )
            
            if payload.get("type") != token_type:
                raise jwt.InvalidTokenError("Invalid token type")
                
            return payload
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

class RateLimiter:
    """Rate limiting for authentication attempts"""
    
    def __init__(self):
        self.attempts = {}  # In production, use Redis
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if authentication attempt is allowed"""
        
        now = datetime.utcnow()
        
        if identifier not in self.attempts:
            return True
            
        attempt_data = self.attempts[identifier]
        
        # Reset if lockout period has passed
        if now > attempt_data["locked_until"]:
            del self.attempts[identifier]
            return True
            
        return attempt_data["count"] < self.max_attempts
    
    def record_attempt(self, identifier: str, success: bool):
        """Record authentication attempt"""
        
        now = datetime.utcnow()
        
        if identifier not in self.attempts:
            self.attempts[identifier] = {"count": 0, "locked_until": now}
        
        if success:
            # Reset on successful authentication
            del self.attempts[identifier]
        else:
            # Increment failed attempts
            self.attempts[identifier]["count"] += 1
            if self.attempts[identifier]["count"] >= self.max_attempts:
                self.attempts[identifier]["locked_until"] = now + self.lockout_duration

class SecurityAuditLogger:
    """Security event audit logging"""
    
    @staticmethod
    def log_login_attempt(
        username: str, 
        success: bool, 
        ip_address: str, 
        user_agent: str,
        failure_reason: str = None
    ):
        """Log authentication attempt"""
        
        logger.info(
            f"Login attempt - Username: {username}, Success: {success}, "
            f"IP: {ip_address}, Reason: {failure_reason or 'N/A'}",
            extra={
                "event_type": "authentication",
                "username": username,
                "success": success,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "failure_reason": failure_reason
            }
        )
    
    @staticmethod
    def log_2fa_attempt(
        username: str,
        success: bool, 
        ip_address: str,
        attempt_type: str = "totp"
    ):
        """Log 2FA attempt"""
        
        logger.info(
            f"2FA attempt - Username: {username}, Success: {success}, "
            f"Type: {attempt_type}, IP: {ip_address}",
            extra={
                "event_type": "two_factor_auth",
                "username": username,
                "success": success,
                "ip_address": ip_address,
                "attempt_type": attempt_type
            }
        )
    
    @staticmethod
    def log_password_change(username: str, ip_address: str):
        """Log password change"""
        
        logger.info(
            f"Password changed - Username: {username}, IP: {ip_address}",
            extra={
                "event_type": "password_change",
                "username": username,
                "ip_address": ip_address
            }
        )
    
    @staticmethod
    def log_security_event(
        event_type: str,
        username: str,
        details: Dict,
        severity: str = "info"
    ):
        """Log generic security event"""
        
        log_func = getattr(logger, severity, logger.info)
        log_func(
            f"Security event - Type: {event_type}, Username: {username}",
            extra={
                "event_type": event_type,
                "username": username,
                **details
            }
        )

class EnhancedAuthenticator:
    """Main authentication class with enhanced security"""
    
    def __init__(self):
        self.jwt_manager = JWTManager()
        self.rate_limiter = RateLimiter()
        self.totp = TwoFactorAuth()
        
    async def authenticate_user(
        self,
        username: str,
        password: str,
        totp_code: str = None,
        request: Request = None,
        db: Session = None
    ) -> AuthResult:
        """
        Authenticate user with enhanced security
        
        Args:
            username: User's username or email
            password: User's password
            totp_code: 2FA TOTP code (if 2FA enabled)
            request: FastAPI request object for device fingerprinting
            db: Database session
            
        Returns:
            AuthResult with authentication status and tokens
        """
        
        client_ip = request.client.host if request and request.client else "unknown"
        user_agent = request.headers.get("user-agent", "") if request else ""
        
        # Rate limiting check
        rate_limit_key = f"{username}:{client_ip}"
        if not self.rate_limiter.is_allowed(rate_limit_key):
            SecurityAuditLogger.log_login_attempt(
                username, False, client_ip, user_agent, "rate_limited"
            )
            raise AuthenticationError("Too many failed attempts. Please try again later.")
        
        try:
            # Step 1: Verify user credentials (mock implementation)
            user = await self._verify_credentials(username, password, db)
            
            if not user:
                self.rate_limiter.record_attempt(rate_limit_key, False)
                SecurityAuditLogger.log_login_attempt(
                    username, False, client_ip, user_agent, "invalid_credentials"
                )
                raise AuthenticationError("Invalid username or password")
            
            # Step 2: Check if 2FA is required
            if user.get("two_factor_enabled"):
                if not totp_code:
                    SecurityAuditLogger.log_login_attempt(
                        username, False, client_ip, user_agent, "2fa_required"
                    )
                    return AuthResult(
                        success=False,
                        requires_2fa=True,
                        message="2FA code required"
                    )
                
                # Verify 2FA code
                if not self.totp.verify_token(user["two_factor_secret"], totp_code):
                    self.rate_limiter.record_attempt(rate_limit_key, False)
                    SecurityAuditLogger.log_2fa_attempt(
                        username, False, client_ip, "totp"
                    )
                    raise TwoFactorError("Invalid 2FA code")
                
                SecurityAuditLogger.log_2fa_attempt(
                    username, True, client_ip, "totp"
                )
            
            # Step 3: Generate session and tokens
            session_id = secrets.token_urlsafe(32)
            device_fingerprint = DeviceFingerprint.generate_fingerprint(request) if request else None
            
            now = datetime.utcnow()
            token_payload = TokenPayload(
                user_id=user["id"],
                session_id=session_id,
                username=user["username"],
                role=user["role"],
                municipality=user["municipality"],
                exp=now + self.jwt_manager.access_token_expire,
                iat=now,
                device_fingerprint=device_fingerprint
            )
            
            access_token = self.jwt_manager.create_access_token(token_payload)
            refresh_token = self.jwt_manager.create_refresh_token(token_payload)
            
            # Step 4: Record successful authentication
            self.rate_limiter.record_attempt(rate_limit_key, True)
            SecurityAuditLogger.log_login_attempt(
                username, True, client_ip, user_agent
            )
            
            # Store session in database (implement as needed)
            await self._store_session(session_id, user["id"], device_fingerprint, db)
            
            return AuthResult(
                success=True,
                user_id=user["id"],
                access_token=access_token,
                refresh_token=refresh_token,
                session_id=session_id,
                message="Authentication successful"
            )
            
        except (AuthenticationError, TwoFactorError):
            self.rate_limiter.record_attempt(rate_limit_key, False)
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            self.rate_limiter.record_attempt(rate_limit_key, False)
            raise AuthenticationError("Authentication failed")
    
    async def _verify_credentials(self, username: str, password: str, db: Session) -> Optional[Dict]:
        """
        Verify user credentials against database
        
        Args:
            username: User's email or username
            password: Plain text password
            db: SQLAlchemy database session
            
        Returns:
            Dict containing user data if authentication succeeds, None otherwise
            
        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            # Query user by email or username
            result = await db.execute(
                select(User).where(
                    (User.email == username) | (User.username == username)
                )
            )
            user = result.scalars().first()
            
            if not user:
                logger.warning(f"User not found: {username}")
                return None
                
            # Verify password
            if not pwd_context.verify(password, user.hashed_password):
                logger.warning(f"Invalid password for user: {username}")
                return None
                
            # Check if user is active
            if not user.is_active:
                logger.warning(f"Inactive user attempted login: {username}")
                return None
                
            # Get user role (assuming a relationship between User and Role models)
            role_name = "user"
            if hasattr(user, 'role') and user.role:
                role_name = user.role.name
            elif hasattr(user, 'is_superuser') and user.is_superuser:
                role_name = "admin"
                
            # Return user data
            return {
                "id": user.id,
                "email": user.email,
                "username": getattr(user, 'username', user.email.split('@')[0]),
                "full_name": getattr(user, 'full_name', ""),
                "is_active": user.is_active,
                "is_superuser": getattr(user, 'is_superuser', False),
                "role": role_name,
                "municipality": getattr(user, 'municipality', ""),
                "two_factor_enabled": getattr(user, 'two_factor_enabled', False),
                "two_factor_secret": getattr(user, 'two_factor_secret', None)
            }
            
        except Exception as e:
            logger.error(f"Error verifying credentials for {username}: {str(e)}")
            raise AuthenticationError("Authentication failed")
    
    async def _store_session(
        self, 
        session_id: str, 
        user_id: int, 
        device_fingerprint: str, 
        db: Session
    ):
        """
        Store session information in database using SessaoSegura model
        
        Args:
            session_id: Unique session identifier
            user_id: ID of the authenticated user
            device_fingerprint: Fingerprint of the device
            db: SQLAlchemy database session
        """
        try:
            from app.models.auth_sessao_segura import SessaoSegura
            
            session_data = {
                "nome": f"Session for user {user_id}",
                "nome_en": f"Session for user {user_id}",
                "descricao": f"Active session for user {user_id}",
                "descricao_en": f"Active session for user {user_id}",
                "dados_adicionais": {
                    "session_id": session_id,
                    "device_fingerprint": device_fingerprint,
                    "last_activity": datetime.utcnow().isoformat()
                },
                "status": "active"
            }
            
            # Create new session record
            db_session = SessaoSegura(**session_data)
            db.add(db_session)
            await db.commit()
            await db.refresh(db_session)
            
            logger.info(f"Session created: {session_id} for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error storing session for user {user_id}: {str(e)}")
            # Don't raise exception to avoid failing the auth flow
            await db.rollback()
    
    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> Dict:
        """
        Get current authenticated user from JWT token
        
        Args:
            credentials: HTTP Authorization credentials containing JWT token
            db: SQLAlchemy database session
            
        Returns:
            Dict containing user information if authentication is successful
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            token = credentials.credentials
            payload = self.jwt_manager.verify_token(token, "access")
            
            # Verify session is still valid (check database)
            session_valid = await self._verify_session(payload.get("session_id"), db)
            if not session_valid:
                raise AuthenticationError("Session expired or invalid")
            
            return {
                "user_id": int(payload["sub"]),
                "username": payload["username"],
                "role": payload["role"],
                "municipality": payload["municipality"],
                "session_id": payload["session_id"]
            }
            
        except AuthenticationError:
            raise HTTPException(status_code=401, detail="Invalid authentication")
    
    async def _verify_session(self, session_id: str, db: Session) -> bool:
        """
        Verify if session is still valid by checking the database
        
        Args:
            session_id: The session ID to verify
            db: SQLAlchemy database session
            
        Returns:
            bool: True if session is valid, False otherwise
        """
        try:
            from app.models.auth_sessao_segura import SessaoSegura
            
            # Find session in database
            result = await db.execute(
                select(SessaoSegura).where(
                    SessaoSegura.dados_adicionais["session_id"].astext == session_id,
                    SessaoSegura.status == "active"
                )
            )
            session = result.scalars().first()
            
            if not session:
                logger.warning(f"Session not found or inactive: {session_id}")
                return False
                
            # Check if session has expired (e.g., 30 minutes of inactivity)
            last_activity = datetime.fromisoformat(session.dados_adicionais.get("last_activity"))
            session_timeout = timedelta(minutes=30)
            
            if datetime.utcnow() - last_activity > session_timeout:
                logger.info(f"Session expired: {session_id}")
                # Mark session as expired in the database
                session.status = "expired"
                await db.commit()
                return False
                
            # Update last activity time
            session.dados_adicionais["last_activity"] = datetime.utcnow().isoformat()
            await db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error verifying session {session_id}: {str(e)}")
            return False

# Global authenticator instance
authenticator = EnhancedAuthenticator()

# Dependency functions
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """FastAPI dependency to get current authenticated user"""
    return authenticator.get_current_user(credentials, db)

async def get_current_admin_user(
    current_user: Dict = Depends(get_current_user)
) -> Dict:
    """FastAPI dependency to require admin role"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Password utilities
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)