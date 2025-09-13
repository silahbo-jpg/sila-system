"""
Token schemas for JWT authentication.
"""
from pydantic import BaseModel, Field

class Token(BaseModel):
    """Schema for access token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type, should be 'bearer'")

class TokenPayload(BaseModel):
    """Payload contained within the JWT token."""
    sub: int | None = Field(None, description="Subject (postgres ID)")
    exp: int | None = Field(None, description="Expiration timestamp")
    scopes: list[str] = Field(default_factory=list, description="List of scopes/roles")

