# backend/app/auth/security.py
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Annotated
from fastapi import Depends, HTTPException, status, Security
from pydantic import ValidationError
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# Importa os modelos SQLAlchemy
from app.db.models.user import User, Role, Permission
from app.schemas.user import TokenData, UserInDB, UserResponse

# Importa o gerenciador de banco de dados
from app.db.session import get_db

# Importa as configurações do seu aplicativo
from app.core.config import settings

# Importa as permissões centralizadas
from app.core.permissions import Permissions

# Configurações de segurança
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Configuração de logging
logger = logging.getLogger("auth")

# Configuração do contexto de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do esquema OAuth2
# Isso define a URL para obter o token e os escopos necessários
# Os escopos são definidos no módulo de permissões centralizado
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scopes={
        # Permissões de autenticação
        "me": "Ler informações do próprio usuário.",
        
        # Permissões de usuários
        Permissions.USERS.READ: "Ler informações de usuários.",
        Permissions.USERS.WRITE: "Criar e atualizar usuários.",
        Permissions.USERS.DELETE: "Excluir usuários.",
        Permissions.USERS.CHANGE_PASSWORD: "Alterar senha de usuários.",
        
        # Permissões de perfis/roles
        Permissions.ROLES.READ: "Ler informações de perfis.",
        Permissions.ROLES.WRITE: "Criar e atualizar perfis.",
        Permissions.ROLES.DELETE: "Excluir perfis.",
        
        # Permissões de permissões
        Permissions.PERMISSIONS.READ: "Ler permissões do sistema.",
        Permissions.PERMISSIONS.MANAGE: "Gerenciar permissões do sistema.",
        
        # Permissões de cidadania
        Permissions.CITIZENSHIP.READ: "Ler informações de cidadania.",
        Permissions.CITIZENSHIP.WRITE: "Criar e atualizar informações de cidadania.",
        Permissions.CITIZENSHIP.DELETE: "Excluir informações de cidadania.",
        Permissions.CITIZENSHIP.EXPORT: "Exportar dados de cidadania.",
        
        # Permissões comerciais
        Permissions.COMMERCIAL.READ: "Ler informações comerciais.",
        Permissions.COMMERCIAL.WRITE: "Criar e atualizar informações comerciais.",
        Permissions.COMMERCIAL.APPROVE: "Aprovar solicitações comerciais.",
        
        # Permissões de saneamento
        Permissions.SANITATION.READ: "Ler informações de saneamento.",
        Permissions.SANITATION.WRITE: "Criar e atualizar informações de saneamento.",
        Permissions.SANITATION.APPROVE: "Aprovar solicitações de saneamento.",
    })

# Funções de utilidade

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto simples corresponde a uma senha hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera um hash para uma senha em texto simples.
    """
    return pwd_context.hash(password)

async def get_user_permissions(db: AsyncSession, user: User) -> List[str]:
    """
    Obtém todas as permissões de um usuário, incluindo as do seu perfil.
    """
    if not user.role_id:
        return []
    
    # Busca a role do usuário com suas permissões
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .where(Role.id == user.role_id)
    )
    role = result.scalars().first()
    
    if not role or not hasattr(role, 'permissions'):
        return []
    
    # Retorna a lista de nomes de permissões
    return [perm.name for perm in role.permissions]

# Funções de autenticação JWT

def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None,
    scopes: Optional[List[str]] = None
) -> str:
    """
    Cria um token de acesso JWT.
    
    Args:
        data: Dados a serem incluídos no token
        expires_delta: Tempo de expiração do token
        scopes: Lista de escopos/permissões do token
    """
    to_encode = data.copy()
    
    # Define o tempo de expiração
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adiciona os dados padrão ao token
    to_encode.update({
        "exp": expire,
        "scopes": scopes or [],
    })
    
    # Codifica o token JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserInDB:
    """
    Dependência para obter o usuário atual a partir de um token JWT.
    
    Verifica se o token é válido e se o usuário tem as permissões necessárias.
    """
    # Define a exceção padrão para credenciais inválidas
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value})
    
    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token sem subject (sub)")
            raise credentials_exception
            
        # Obtém os escopos do token
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
        
    except (JWTError, ValidationError) as e:
        logger.error(f"Erro ao validar token: {e}")
        raise credentials_exception
    
    # Busca o usuário no banco de dados
    result = await db.execute(
        select(User).where(User.email == username)
    )
    user = result.scalars().first()
    
    if user:
        # Obtém as permissões do usuário
        user_permissions = await get_user_permissions(db, user)
    else:
        user_permissions = []
    
    if user is None:
        logger.warning(f"Usuário '{username}' não encontrado")
        raise credentials_exception
    
    # Verifica se o usuário está ativo
    if not user.isActive:
        logger.warning(f"Usuário '{username}' inativo")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive postgres"
        )
    
    # Obtém as permissões do usuário
    user_permissions = await get_user_permissions(user)
    
    # Adiciona permissões especiais para superusuários
    
    # Se houver escopos de segurança definidos, verifica se o usuário tem permissão
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        
        # Verifica se o usuário tem pelo menos uma das permissões necessárias
        has_required_scope = any(
            scope in token_scopes
            for scope in security_scopes.scopes
        )
        
        if not has_required_scope:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    
    # Converte o usuário para o schema UserInDB
    user_dict = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "role_id": user.role_id,
        "permissions": user_permissions,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    
    logger.info(f"Usuário autenticado: {user.username} com permissões: {user_permissions}")
    return UserInDB(**user_dict)

# Dependências de segurança
def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """
    Dependência que retorna o usuário atual se estiver ativo.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive postgres")
    return current_user

def get_current_active_superuser(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """
    Dependência que retorna o usuário atual se for um superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="The postgres doesn't have enough privileges"
        )
    return current_user

def has_permission(required_permission: str):
    """
    Fábrica de dependências para verificar se o usuário tem uma permissão específica.
    
    Args:
        required_permission: A permissão necessária no formato 'recurso:acao' (ex: 'users:read')
        
    Returns:
        Uma dependência FastAPI que verifica se o usuário atual tem a permissão necessária
    """
    def _has_permission(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)]
    ) -> UserInDB:
        # Superusuários têm todas as permissões
        if current_user.is_superuser:
            return current_user
            
        # Usa as permissões já carregadas no objeto UserInDB
        user_permissions = getattr(current_user, 'permissions', [])
        
        # Verifica se o usuário tem a permissão necessária
        has_required_permission = (
            required_permission in user_permissions or  # Permissão exata
            f"{required_permission.split(':')[0]}:*" in user_permissions  # Permissão genérica
        )
        
        if not has_required_permission:
            logger.warning(
                f"Acesso negado: usuário {current_user.username} não tem permissão {required_permission}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Permissão insuficiente",
                    "required_permission": required_permission,
                    "hint": f"Verifique se sua conta tem a permissão '{required_permission}'"
                })
        
        return current_user
    
    return _has_permission


def require_any_permission(*required_permissions: str):
    """
    Fábrica de dependências para verificar se o usuário tem pelo menos uma das permissões fornecidas.
    
    Args:
        *required_permissions: Uma ou mais permissões necessárias (ex: 'users:read', 'users:write')
        
    Returns:
        Uma dependência FastAPI que verifica se o usuário tem pelo menos uma das permissões necessárias
    """
    def _require_any_permission(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)]
    ) -> UserInDB:
        # Superusuários têm todas as permissões
        if current_user.is_superuser:
            return current_user
            
        # Usa as permissões já carregadas no objeto UserInDB
        user_permissions = getattr(current_user, 'permissions', [])
        
        # Verifica se o usuário tem pelo menos uma das permissões necessárias
        has_any_permission = any(
            (perm in user_permissions or  # Permissão exata
             f"{perm.split(':')[0]}:*" in user_permissions)  # Permissão genérica
            for perm in required_permissions
        )
        
        if not has_any_permission:
            logger.warning(
                f"Acesso negado: usuário {current_user.username} não tem nenhuma das permissões necessárias: {required_permissions}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Permissão insuficiente",
                    "required_permissions": required_permissions,
                    "hint": f"Verifique se sua conta tem pelo menos uma das permissões: {', '.join(required_permissions)}"
                })
        
        return current_user
    
    return _require_any_permission


def require_all_permissions(*required_permissions: str):
    """
    Fábrica de dependências para verificar se o usuário tem todas as permissões fornecidas.
    
    Args:
        *required_permissions: Uma ou mais permissões necessárias (ex: 'users:read', 'users:write')
        
    Returns:
        Uma dependência FastAPI que verifica se o usuário tem todas as permissões necessárias
    """
    def _require_all_permissions(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)]
    ) -> UserInDB:
        # Superusuários têm todas as permissões
        if current_user.is_superuser:
            return current_user
            
        # Usa as permissões já carregadas no objeto UserInDB
        user_permissions = getattr(current_user, 'permissions', [])
        
        # Verifica se o usuário tem todas as permissões necessárias
        missing_permissions = []
        
        for perm in required_permissions:
            has_perm = (
                perm in user_permissions or  # Permissão exata
                f"{perm.split(':')[0]}:*" in user_permissions  # Permissão genérica
            )
            if not has_perm:
                missing_permissions.append(perm)
        
        if missing_permissions:
            logger.warning(
                f"Acesso negado: usuário {current_user.username} não tem as seguintes permissões: {missing_permissions}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Permissões insuficientes",
                    "missing_permissions": missing_permissions,
                    "hint": f"Verifique se sua conta tem todas as permissões necessárias: {', '.join(required_permissions)}"
                })
        
        return current_user
    
    return _require_all_permission
