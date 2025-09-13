"""Testes isolados para o sistema de permissões do módulo de cidadania.

Este arquivo contém testes que não dependem do banco de dados ou do conftest.py global.
"""
import pytest
from fastapi import HTTPException, status
from pydantic import BaseModel


class MockUserInDB(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    permissions: list[str] = []


class MockPermissions:
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


# Fixtures locais

@pytest.fixture
def mock_user():
    return MockUserInDB(
        id=1,
        username="testuser",
        email="test@example.com",
        full_name="Test postgres",
        permissions=["citizenship:citizen:read", "citizenship:document:download"]
    )


@pytest.fixture
def mock_superuser():
    return MockUserInDB(
        id=2,
        username="postgres",
        email="postgres",
        full_name="postgres postgres",
        is_superuser=True,
        permissions=[]
    )


# Função mock para has_permission

async def mock_has_permission(required_permission: str, current_user: MockUserInDB):
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


# Testes

class TestPermissions:
    def test_all_permissions(self):
        perms = MockPermissions.all_permissions()
        assert isinstance(perms, list)
        assert len(perms) > 0
        assert all(isinstance(p, str) for p in perms)
        assert all(p.startswith('citizenship:') for p in perms)

    @pytest.mark.asyncio
    async def test_has_permission_success(self, mock_user):
        # Testa permissão concedida
        result = await mock_has_permission("citizenship:citizen:read", mock_user)
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_has_permission_denied(self, mock_user):
        # Testa permissão não concedida
        with pytest.raises(HTTPException) as exc_info:
            await mock_has_permission("citizenship:citizen:create", mock_user)
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_superuser_has_all_permissions(self, mock_superuser):
        # Testa que superusuário tem todas as permissões
        result = await mock_has_permission("any:permission", mock_superuser)
        assert result == mock_superuser

