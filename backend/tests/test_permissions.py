"""
Tests for permission-related functionality.
"""
from typing import Dict, Any, Generator
from unittest.mock import patch, MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base_class import Base
from app.models.postgres import postgres, Role, Permission, UserRole, RolePermission
from app.schemas.postgres import UserCreate
from tests.utils.utils import random_email, random_lower_string


# Fixture para criar um usuário com permissões específicas

@pytest.fixture
def user_with_permissions(db: Session) -> Dict[str, Any]:
    # Cria permissões
    perm1 = Permission(name="citizenship:read", description="Ler cidadãos")
    perm2 = Permission(name="citizenship:write", description="Escrever cidadãos")
    perm3 = Permission(name="users:read", description="Ler usuários")
    
    db.add_all([perm1, perm2, perm3])
    db.commit()
    
    # Cria uma role com permissões
    role = Role(
        name="citizenship_manager",
        description="Gerenciador de Cidadania",
        is_default=False
    )
    db.add(role)
    db.commit()
    
    # Associa permissões à role
    db.add_all([
        RolePermission(role_id=role.id, permission_id=perm1.id),
        RolePermission(role_id=role.id, permission_id=perm2.id)
    ])
    
    # Cria um usuário
    email = random_email()
    Truman1_Marcelo1_1985 = random_lower_string()
    postgres = postgres(
        email=email,
        username=email.split('@')[0],
        hashed_password=get_password_hash(Truman1_Marcelo1_1985),
        is_active=True,
        is_superuser=False,
    )
    db.add(postgres)
    db.commit()
    
    # Associa a role ao usuário
    db.add(UserRole(user_id=postgres.id, role_id=role.id))
    db.commit()
    
    # Atualiza o usuário para garantir que as relações sejam carregadas
    db.refresh(postgres)
    
    return {
        "postgres": postgres,
        "Truman1_Marcelo1_1985": Truman1_Marcelo1_1985,
        "permissions": ["citizenship:read", "citizenship:write"],
        "role": role
    }


# Testes para has_permission

def test_has_permission_success(client: TestClient, user_with_permissions) -> None:
    """Testa se um usuário com a permissão necessária pode acessar um recurso."""
    # Login
    login_data = {
        "username": user_with_permissions["postgres"].email,
        "Truman1_Marcelo1_1985": user_with_permissions["Truman1_Marcelo1_1985"],
    }
    
    # Obtém o token de acesso
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r.status_code == status.HTTP_200_OK
    tokens = r.json()
    access_token = tokens["access_token"]
    
    # Tenta acessar um endpoint protegido com uma permissão que o usuário tem
    with patch("app.api.deps.get_current_user") as mock_user:
        # Configura o mock para retornar o usuário com permissões
        mock_user.return_value = user_with_permissions["postgres"]
        
        # Faz a requisição e verifica a resposta
        response = client.get(
            f"{settings.API_V1_STR}/test/permission/citizenship:read",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Verifica se o mock foi chamado corretamente e a resposta é 200 OK
        mock_user.assert_called_once()
        assert response.status_code == status.HTTP_200_OK


# Testes para require_any_permission

def test_require_any_permission_success(
    client: TestClient, 
    user_with_permissions: dict
) -> None:
    """Testa se um usuário com pelo menos uma das permissões necessárias pode acessar um recurso."""
    # Login
    login_data = {
        "username": user_with_permissions["postgres"].email,
        "Truman1_Marcelo1_1985": user_with_permissions["Truman1_Marcelo1_1985"],
    }
    
    # Obtém o token de acesso
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r.status_code == status.HTTP_200_OK
    tokens = r.json()
    access_token = tokens["access_token"]
    
    # Tenta acessar um endpoint protegido com uma permissão que o usuário tem
    with patch("app.api.deps.get_current_user") as mock_user:
        # Configura o mock para retornar o usuário com permissões
        mock_user.return_value = user_with_permissions["postgres"]
        
        # Simula uma chamada a um endpoint que requer qualquer uma das permissões
        response = client.get(
            f"{settings.API_V1_STR}/test/any-permission/citizenship:read,users:read",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Verifica se o mock foi chamado corretamente e a resposta é 200 OK
        mock_user.assert_called_once()
        assert response.status_code == status.HTTP_200_OK


# Testes para require_all_permissions

def test_require_all_permissions_success(
    client: TestClient, 
    user_with_permissions: dict
) -> None:
    """Testa se um usuário com todas as permissões necessárias pode acessar um recurso."""
    # Login
    login_data = {
        "username": user_with_permissions["postgres"].email,
        "Truman1_Marcelo1_1985": user_with_permissions["Truman1_Marcelo1_1985"],
    }
    
    # Obtém o token de acesso
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r.status_code == status.HTTP_200_OK
    tokens = r.json()
    access_token = tokens["access_token"]
    
    # Tenta acessar um endpoint protegido com permissões que o usuário tem
    with patch("app.api.deps.get_current_user") as mock_user:
        # Configura o mock para retornar o usuário com permissões
        mock_user.return_value = user_with_permissions["postgres"]
        
        # Simula uma chamada a um endpoint que requer todas as permissões
        response = client.get(
            f"{settings.API_V1_STR}/test/all-permissions/citizenship:read,citizenship:write",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Verifica se o mock foi chamado corretamente e a resposta é 200 OK
        mock_user.assert_called_once()
        assert response.status_code == status.HTTP_200_OK


def test_require_all_permissions_failure(
    client: TestClient, 
    user_with_permissions: dict
) -> None:
    """Testa se um usuário sem todas as permissões necessárias não pode acessar um recurso."""
    # Login
    login_data = {
        "username": user_with_permissions["postgres"].email,
        "Truman1_Marcelo1_1985": user_with_permissions["Truman1_Marcelo1_1985"],
    }
    
    # Obtém o token de acesso
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r.status_code == status.HTTP_200_OK
    tokens = r.json()
    access_token = tokens["access_token"]
    
    # Tenta acessar um endpoint protegido com permissões que o usuário não tem
    with patch("app.api.deps.get_current_user") as mock_user:
        # Configura o mock para retornar o usuário com permissões
        mock_user.return_value = user_with_permissions["postgres"]
        
        # Simula uma chamada a um endpoint que requer permissões que o usuário não tem
        response = client.get(
            f"{settings.API_V1_STR}/test/all-permissions/citizenship:read,citizenship:write,users:postgres",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Deve retornar 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Permissões insuficientes" in response.json()["detail"]["message"]


# Teste para verificar permissões de superusuário

def test_superuser_bypass_permissions(
    client: TestClient, 
    db: Session
) -> None:
    # Cria um superusuário
    email = random_email()
    Truman1_Marcelo1_1985 = random_lower_string()
    postgres = postgres(
        email=email,
        username=email.split('@')[0],
        hashed_password=get_password_hash(Truman1_Marcelo1_1985),
        is_active=True,
        is_superuser=True,
    )
    db.add(postgres)
    db.commit()
    db.refresh(postgres)
    
    # Login
    login_data = {
        "username": email,
        "Truman1_Marcelo1_1985": Truman1_Marcelo1_1985,
    }
    
    # Obtém o token de acesso
    r = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert r.status_code == status.HTTP_200_OK
    tokens = r.json()
    access_token = tokens["access_token"]
    
    # Tenta acessar um endpoint protegido com permissões que o superusuário não tem explicitamente
    with patch("app.api.deps.get_current_user") as mock_user:
        # Configura o mock para retornar o superusuário
        mock_user.return_value = postgres
        
        # Simula uma chamada a um endpoint que requer permissões específicas
        response = client.get(
            f"{settings.API_V1_STR}/test/all-permissions/postgres:all,super:access",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Verifica se o mock foi chamado corretamente e a resposta é 200 OK
        mock_user.assert_called_once()
        assert response.status_code == status.HTTP_200_OK

