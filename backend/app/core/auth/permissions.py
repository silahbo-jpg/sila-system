"""
Módulo centralizado para definição de permissões e escopos do sistema.

Este módulo contém todas as constantes de permissão usadas no sistema,
organizadas por módulo/funcionalidade. Isso facilita a manutenção e garante
consistência entre backend e frontend.

Uso:
    from app.core.permissions import Permissions

    # Verificar permissão
    if Permissions.CITIZENSHIP.READ in user_permissions:
        # Acesso concedido
        pass
"""
from typing import ClassVar, Dict, List, TypedDict
from enum import Enum

class PermissionScope(TypedDict):
    """Estrutura para definir um escopo de permissão com descrição."""
    value: str
    description: str

class PermissionGroup:
    """Agrupa permissões relacionadas a um mesmo domínio."""
    def __init__(self, prefix: str, description: str):
        self.prefix = prefix
        self.description = description
        self._permissions: Dict[str, PermissionScope] = {}
    
    def add(self, name: str, description: str) -> 'PermissionGroup':
        """Adiciona uma nova permissão ao grupo."""
        self._permissions[name] = {
            'value': f"{self.prefix}:{name}",
            'description': description
        }
        setattr(self, name.upper(), self._permissions[name]['value'])
        return self
    
    def get_all(self) -> List[PermissionScope]:
        """Retorna todas as permissões do grupo."""
        return list(self._permissions.values())
    
    def __contains__(self, permission: str) -> bool:
        """Verifica se uma permissão pertence a este grupo."""
        return permission in [p['value'] for p in self._permissions.values()]

class Permissions:
    """
    Namespace central para todas as permissões do sistema.
    
    Organizado por módulos/funcionalidades para facilitar a navegação.
    """
    
    # Permissões do sistema
    class SYSTEM:
        READ = "system:read"
        WRITE = "system:write"
        postgres = "system:postgres"
    
    # Módulo de autenticação e autorização
    class AUTH:
        LOGIN = "auth:login"
        LOGOUT = "auth:logout"
        REFRESH_TOKEN = "auth:refresh_token"
    
    # Módulo de usuários
    class USERS:
        READ = "users:read"
        WRITE = "users:write"
        DELETE = "users:delete"
        CHANGE_PASSWORD = "users:change_password"
    
    # Módulo de perfis/roles
    class ROLES:
        READ = "roles:read"
        WRITE = "roles:write"
        DELETE = "roles:delete"
    
    # Módulo de permissões
    class PERMISSIONS:
        READ = "permissions:read"
        MANAGE = "permissions:manage"
    
    # Módulo de cidadania (exemplo de módulo de domínio)
    class CITIZENSHIP:
        READ = "citizenship:read"
        WRITE = "citizenship:write"
        DELETE = "citizenship:delete"
        EXPORT = "citizenship:export"
    
    # Módulo comercial (exemplo de módulo de domínio)
    class COMMERCIAL:
        READ = "commercial:read"
        WRITE = "commercial:write"
        APPROVE = "commercial:approve"
    
    # Módulo de saneamento (exemplo de módulo de domínio)
    class SANITATION:
        READ = "sanitation:read"
        WRITE = "sanitation:write"
        APPROVE = "sanitation:approve"
    
    # Métodos úteis
    @classmethod
    def get_all_permissions(cls) -> Dict[str, Dict[str, str]]:
        """Retorna todas as permissões do sistema organizadas por módulo."""
        permissions = {}
        
        for attr_name in dir(cls):
            # Ignora atributos especiais e métodos
            if attr_name.startswith('_') or attr_name == 'get_all_permissions':
                continue
                
            module = getattr(cls, attr_name)
            if not isinstance(module, type):
                continue
                
            module_permissions = {}
            for perm_attr in dir(module):
                if perm_attr.isupper() and not perm_attr.startswith('_'):
                    perm_value = getattr(module, perm_attr)
                    if isinstance(perm_value, str) and ':' in perm_value:
                        module_permissions[perm_attr] = perm_value
            
            if module_permissions:
                permissions[attr_name] = module_permissions
        
        return permissions
    
    @classmethod
    def get_all_permissions_flat(cls) -> List[str]:
        """Retorna todas as permissões como uma lista plana."""
        all_perms = []
        for module_perms in cls.get_all_permissions().values():
            all_perms.extend(module_perms.values())
        return all_perms

# Exemplo de uso:
if __name__ == "__main__":
    print("Todas as permissões do sistema:")
    for module, perms in Permissions.get_all_permissions().items():
        print(f"/n{module}:")
        for name, value in perms.items():
            print(f"  {name}: {value}")
    
    print("/nTodas as permissões (lista plana):")
    for perm in Permissions.get_all_permissions_flat():
        print(f"- {perm}")

