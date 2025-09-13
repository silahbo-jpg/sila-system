#!/usr/bin/env python3
"""
Script para corrigir completamente o arquivo backend/app/schemas/user.py
com formatação e estrutura adequadas, compatível com Pydantic v2.
"""

from pathlib import Path


def fix_user_py() -> bool:
    """Corrige o arquivo user.py com conteúdo já padronizado."""
    file_path = Path("backend/app/schemas/user.py")
    backup_path = file_path.with_suffix(f"{file_path.suffix}.complete_bak")

    print(f"🔧 Processando: {file_path}")

    try:
        # Criar backup do arquivo original
        if file_path.exists():
            original_content = file_path.read_text(encoding="utf-8")
            backup_path.write_text(original_content, encoding="utf-8")
            print(f"  📦 Backup criado em: {backup_path}")

        # Conteúdo corrigido (com base nas diretivas definidas)
        fixed_content = '''# backend/app/schemas/user.py
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.security import validate_password_strength, is_password_compromised


# ================================================================
# Usuário Base
# ================================================================
class UserBase(BaseModel):
    """Base schema para dados de usuário."""
    email: EmailStr = Field(..., json_schema_extra={"example": "johndoe@example.com"})
    name: str = Field(..., json_schema_extra={"example": "John Doe"}, max_length=100)
    role: str = Field("user", json_schema_extra={"example": "user"})
    user_type: str = Field("citizen", json_schema_extra={"example": "citizen"})
    is_active: bool = Field(True, json_schema_extra={"example": True})
    municipality_id: Optional[int] = Field(None, json_schema_extra={"example": 1})


class UserCreate(UserBase):
    """Schema para criação de usuário."""
    password: str = Field(..., min_length=12, json_schema_extra={"example": "SenhaSegura123!@#"})

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        is_valid, errors = validate_password_strength(v)
        if not is_valid:
            raise ValueError(" ".join(errors))

        if is_password_compromised(v):
            raise ValueError(
                "Esta senha foi comprometida em vazamentos de dados. Por favor, escolha uma senha mais segura."
            )
        return v


class UserResponse(UserBase):
    """Schema para resposta de usuário."""
    id: int = Field(..., json_schema_extra={"example": 1})
    created_at: datetime = Field(..., json_schema_extra={"example": "2023-01-01T00:00:00"})
    updated_at: datetime = Field(..., json_schema_extra={"example": "2023-01-01T00:00:00"})

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserResponse):
    """Schema para usuário no banco de dados com informações sensíveis."""
    hashed_password: str = Field(..., alias="hashed_password")
    failed_attempts: int = Field(default=0)
    last_login: Optional[datetime] = None
    locked_until: Optional[datetime] = None
    permissions: List[str] = Field(
        default_factory=list,
        description="Lista de permissões do usuário, incluindo as do seu perfil",
    )

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "johndoe@example.com",
                "name": "John Doe",
                "role": "user",
                "user_type": "citizen",
                "is_active": True,
                "municipality_id": 1,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "failed_attempts": 0,
                "last_login": None,
                "locked_until": None,
                "permissions": ["users:read", "citizenship:read"],
            }
        },
    )


# ================================================================
# Tokens
# ================================================================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "johndoe"})


# ================================================================
# Permissões e Papéis
# ================================================================
class PermissionBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Permission Name"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Permission description"})


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "admin"})
    description: str = Field(..., json_schema_extra={"example": "Administrador do sistema"})
    is_default: bool = Field(False, json_schema_extra={"example": False})


class RoleCreate(RoleBase):
    permission_ids: List[int] = Field(default_factory=list, json_schema_extra={"example": [1, 2, 3]})


class RoleUpdate(RoleBase):
    name: Optional[str] = Field(None, json_schema_extra={"example": "admin_updated"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Descrição atualizada"})
    permission_ids: Optional[List[int]] = Field(None, json_schema_extra={"example": [1, 2, 3, 4]})


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ================================================================
# Perfil de Usuário
# ================================================================
class UserProfileResponse(UserResponse):
    role: Optional[RoleResponse] = None
    permissions: List[str] = []

    @classmethod
    def from_user_with_role(
        cls, user: UserInDB, role: Optional[RoleResponse] = None, permissions: Optional[List[str]] = None
    ):
        user_dict = user.model_dump(exclude={"hashed_password"})
        return cls(**user_dict, role=role, permissions=permissions or [])


# ================================================================
# Atualização de Senha
# ================================================================
class PasswordUpdate(BaseModel):
    current_password: str = Field(..., json_schema_extra={"example": "SenhaAtual123!@#"})
    new_password: str = Field(..., min_length=12, json_schema_extra={"example": "NovaSenhaRobustaInstitucional!!@#"})

    @field_validator("new_password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        is_valid, errors = validate_password_strength(v)
        if not is_valid:
            raise ValueError(" ".join(errors))

        if is_password_compromised(v):
            raise ValueError(
                "Esta senha foi comprometida em vazamentos de dados. Por favor, escolha uma senha mais segura."
            )
        return v


# ================================================================
# Redefinição de Senha
# ================================================================
class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "user@example.com"})


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., json_schema_extra={"example": "reset_token_here"})
    new_password: str = Field(..., min_length=12, json_schema_extra={"example": "NovaSenhaRobustaInstitucional!!@#"})

    @field_validator("new_password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        is_valid, errors = validate_password_strength(v)
        if not is_valid:
            raise ValueError(" ".join(errors))

        if is_password_compromised(v):
            raise ValueError(
                "Esta senha foi comprometida em vazamentos de dados. Por favor, escolha uma senha mais segura."
            )
        return v
'''

        # Escrever conteúdo corrigido no arquivo
        file_path.write_text(fixed_content, encoding="utf-8")
        print("✅ Arquivo user.py atualizado com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")

        # Restaurar backup em caso de erro
        if backup_path.exists():
            file_path.write_text(backup_path.read_text(encoding="utf-8"), encoding="utf-8")
            print("  🔄 Arquivo restaurado a partir do backup.")
        return False


if __name__ == "__main__":
    fix_user_py()
