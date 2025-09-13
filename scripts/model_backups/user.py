"""
User model for the application.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID as UUIDType

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=True)
    
    # Autenticação
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_verified = Column(Boolean(), default=False)
    
    # Dados do usuário
    full_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    
    # Controle de acesso
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    role = relationship('Role', back_populates='users')
    
    # Status e auditoria
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    # Tokens de redefinição
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime(timezone=True), nullable=True)
    verification_token = Column(String(255), nullable=True)
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    permissions = relationship('Permission', secondary='user_permissions', back_populates='users')
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_locked(self) -> bool:
        """Verifica se a conta do usuário está bloqueada."""
        if self.locked_until is None:
            return False
        return self.locked_until > datetime.utcnow()
    
    def get_permissions(self) -> List[str]:
        """Retorna todas as permissões do usuário, incluindo as do seu perfil."""
        permissions = set()
        
        # Adiciona permissões diretas do usuário
        for perm in self.permissions:
            permissions.add(perm.name)
        
        # Adiciona permissões do perfil (role)
        if self.role:
            for perm in self.role.permissions:
                permissions.add(perm.name)
        
        return list(permissions)


class Role(Base):
    """Modelo para perfis de usuário."""
    
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_default = Column(Boolean, default=False)
    
    # Relacionamentos
    users = relationship('User', back_populates='role')
    permissions = relationship('Permission', secondary='role_permissions', back_populates='roles')
    
    def __repr__(self):
        return f"<Role {self.name}>"


class Permission(Base):
    """Modelo para permissões."""
    
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relacionamentos
    roles = relationship('Role', secondary='role_permissions', back_populates='permissions')
    users = relationship('User', secondary='user_permissions', back_populates='permissions')
    
    def __repr__(self):
        return f"<Permission {self.name}>"


# Tabelas de associação
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

user_permissions = Table(
    'user_permissions',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)
