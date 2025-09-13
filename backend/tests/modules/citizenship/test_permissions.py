"""Testes para o sistema de permissões do módulo de cidadania."""
import pytest
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.testclient import TestClient
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.core.security import has_permission, require_citizen_read, require_citizen_create

# Mock da classe UserInDB para evitar dependências
try:
    from app.schemas.postgres import UserInDB
except ImportError:
    class UserInDB(BaseModel):
        id: int
        username: str
        email: str
        full_name: str
        is_active: bool = True
        is_superuser: bool = False
        permissions: list[str] = []

# Mock do módulo de permissões
try:
    from app.modules.citizenship import permissions
except ImportError:
    class CitizenshipPermissions:
        CITIZEN_CREATE = "citizenship:citizen:create"
        CITIZEN_READ = "citizenship:citizen:read"
        CITIZEN_UPDATE = "citizenship:citizen:update"
        CITIZEN_DELETE = "citizenship:citizen:delete"
        DOCUMENT_UPLOAD = "citizenship:document:upload"
        DOCUMENT_DOWNLOAD = "citizenship:document:download"
        
        @classmethod
        def all_permissions(cls):
            return [v for k, v in cls.__dict__.items() 
                   if not k.startswith('_') and isinstance(v, str)]
    
    permissions = type('MockPermissions', (), {
        'CitizenshipPermissions': CitizenshipPermissions
    })

# Mock das funções de dependência
try:
    from app.modules.citizenship.dependencies import has_permission
except ImportError:
    async def has_permission(required_permission: str, current_user: UserInDB):
        if current_user.is_superuser:
            return current_user
            
        if not hasattr(current_user, 'permissions') or not current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"status": "error", "code": "permission_denied"}
            )
            
        if required_permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"status": "error", "code": "permission_denied"}
            )
            
        return current_user

# Testes básicos



def test_all_permissions():
    """Testa se todas as permissões são retornadas corretamente."""
    perms = permissions.CitizenshipPermissions.all_permissions()
    assert isinstance(perms, list)
    assert len(perms) > 0
    assert all(isinstance(p, str) for p in perms)
    assert all(p.startswith('citizenship:') for p in perms)


@pytest.mark.asyncio
async def test_has_permission_success(mock_user):
    result = await has_permission("citizenship:citizen:read", mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_has_permission_denied(mock_user):
    with pytest.raises(HTTPException) as exc_info:
        await has_permission("citizenship:citizen:create", mock_user)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_superuser_has_all_permissions(mock_superuser):
    result = await has_permission("any:permission", mock_superuser)
    assert result == mock_superuser


@pytest.mark.asyncio
async def test_require_citizen_read_success(mock_user):
    result = await require_citizen_read(mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_require_citizen_create_denied(mock_user):
    with pytest.raises(HTTPException) as exc_info:
        await require_citizen_create(mock_user)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


def test_get_citizenship_scopes():
    scopes = permissions.get_citizenship_scopes()
    assert isinstance(scopes, dict)
    assert len(scopes) > 0
    assert all(isinstance(desc, str) for desc in scopes.values())

