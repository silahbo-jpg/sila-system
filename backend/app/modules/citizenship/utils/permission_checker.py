"""
Script para verificar permissões nas rotas do módulo de cidadania.

Este script analisa as rotas do módulo de cidadania e verifica se cada rota
está devidamente protegida com as permissões necessárias.
"""
import inspect
import os
import sys
from typing import Dict, List, Optional, Tuple, Any, Set
from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute

# Adiciona o diretório raiz ao path para importações absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

# Importa o roteador do módulo de cidadania
from app.modules.citizenship.endpoints import router as citizenship_router
from app.modules.citizenship import permissions as citizenship_permissions

# Mapeamento de métodos HTTP para permissões esperadas
METHOD_TO_PERMISSION = {
    'GET': 'read',
    'POST': 'create',
    'PUT': 'update',
    'DELETE': 'delete',
    'PATCH': 'update',
}

# Mapeamento de prefixos de rota para tipos de recurso
PATH_PREFIX_TO_RESOURCE = {
    '/api/citizenship/citizens': 'citizen',
    '/api/citizenship/documents': 'document',
    '/api/citizenship/family': 'family',
    '/api/citizenship/feedback': 'feedback',
}

class PermissionCheckResult:
    """Resultado da verificação de permissões para uma rota."""
    
    def __init__(self, path: str, methods: List[str]):
        self.path = path
        self.methods = methods
        self.checks: Dict[str, Dict[str, Any]] = {}
        
    def add_check(self, method: str, has_auth: bool, permission: Optional[str] = None, 
                 has_dependency: bool = False, dependency_name: str = None):
        """Adiciona o resultado da verificação para um método HTTP."""
        self.checks[method] = {
            'has_auth': has_auth,
            'required_permission': permission,
            'has_dependency': has_dependency,
            'dependency_name': dependency_name,
            'is_secure': has_auth and (permission is not None or has_dependency)
        }
    
    def is_secure(self) -> bool:
        """Verifica se a rota está totalmente protegida para todos os métodos."""
        if not self.checks:
            return False
        return all(check['is_secure'] for check in self.checks.values())
    
    def get_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Retorna uma lista de vulnerabilidades encontradas na rota."""
        vulnerabilities = []
        for method, check in self.checks.items():
            if not check['is_secure']:
                vuln = {
                    'method': method,
                    'path': self.path,
                    'issues': []
                }
                if not check['has_auth']:
                    vuln['issues'].append('Falta autenticação')
                if not check['has_dependency'] and check['required_permission']:
                    vuln['issues'].append(f'Falta verificação de permissão para: {check["required_permission"]}')
                vulnerabilities.append(vuln)
        return vulnerabilities


def get_route_permission(route_path: str, method: str) -> Optional[str]:
    """Determina a permissão necessária para uma rota com base no caminho e método."""
    # Remove parâmetros de rota para correspondência
    base_path = route_path.split('{', 1)[0].rstrip('/')
    
    # Encontra o recurso correspondente ao prefixo da rota
    resource_type = None
    for prefix, resource in PATH_PREFIX_TO_RESOURCE.items():
        if base_path.startswith(prefix):
            resource_type = resource
            break
    
    if not resource_type:
        return None
    
    # Obtém o tipo de ação com base no método HTTP
    action = METHOD_TO_PERMISSION.get(method)
    if not action:
        return None
    
    # Retorna a permissão no formato esperado
    return f"citizenship:{resource_type}:{action}"


def check_route_dependencies(route: APIRoute) -> Tuple[bool, Optional[str]]:
    """
    Verifica as dependências de uma rota para autenticação e permissões.
    
    Retorna:
        Tuple[bool, Optional[str]]: (tem_autenticacao, nome_da_dependencia_de_permissao)
    """
    has_auth = False
    permission_dependency = None
    
    # Verifica as dependências da rota
    dependencies = route.dependencies or []
    for dep in dependencies:
        # Verifica se há uma dependência de autenticação
        if hasattr(dep, 'call') and 'current_user' in inspect.signature(dep.call).parameters:
            has_auth = True
        
        # Verifica se há uma dependência de permissão
        if hasattr(dep, 'call') and 'require_' in str(dep.call.__qualname__):
            permission_dependency = dep.call.__qualname__
    
    return has_auth, permission_dependency


def check_routes_security(router: APIRouter) -> Dict[str, PermissionCheckResult]:
    """
    Verifica a segurança das rotas em um roteador FastAPI.
    
    Args:
        router: Roteador FastAPI a ser verificado
        
    Returns:
        Dict[str, PermissionCheckResult]: Dicionário com os resultados da verificação
    """
    results = {}
    
    for route in router.routes:
        if not isinstance(route, APIRoute):
            continue
            
        # Cria um resultado para a rota se ainda não existir
        if route.path not in results:
            results[route.path] = PermissionCheckResult(route.path, [])
        
        # Verifica as dependências da rota
        has_auth, permission_dependency = check_route_dependencies(route)
        
        # Determina a permissão necessária com base no caminho e método
        required_permission = get_route_permission(route.path, route.methods.pop())
        
        # Adiciona a verificação para cada método da rota
        for method in route.methods:
            results[route.path].methods.append(method)
            results[route.path].add_check(
                method=method,
                has_auth=has_auth,
                permission=required_permission,
                has_dependency=permission_dependency is not None,
                dependency_name=permission_dependency
            )
    
    return results


def generate_security_report() -> Dict[str, Any]:
    """Gera um relatório de segurança para as rotas do módulo de cidadania."""
    # Verifica as rotas do módulo de cidadania
    results = check_routes_security(citizenship_router)
    
    # Contadores para o relatório
    total_routes = len(results)
    secure_routes = 0
    vulnerabilities = []
    
    # Analisa os resultados
    for path, result in results.items():
        if result.is_secure():
            secure_routes += 1
        else:
            vulnerabilities.extend(result.get_vulnerabilities())
    
    # Gera o relatório
    report = {
        'module': 'citizenship',
        'total_routes': total_routes,
        'secure_routes': secure_routes,
        'insecure_routes': total_routes - secure_routes,
        'security_score': f"{(secure_routes / total_routes * 100):.1f}%" if total_routes > 0 else 'N/A',
        'vulnerabilities': vulnerabilities,
        'recommendations': [
            'Adicione autenticação a todas as rotas que manipulam dados sensíveis',
            'Use as dependências de permissão para controlar o acesso a recursos',
            'Implemente verificações adicionais de autorização nos serviços',
            'Considere usar escopos OAuth2 para um controle de acesso mais granular'
        ]
    }
    
    return report


def print_security_report():
    """Imprime um relatório de segurança no console."""
    report = generate_security_report()
    
    print("\n" + "="*80)
    print(f"RELATÓRIO DE SEGURANÇA - MÓDULO {report['module'].upper()}")
    print("="*80)
    print(f"Total de rotas: {report['total_routes']}")
    print(f"Rotas seguras: {report['secure_routes']}")
    print(f"Rotas inseguras: {report['insecure_routes']}")
    print(f"Pontuação de segurança: {report['security_score']}")
    
    if report['vulnerabilities']:
        print("\nVULNERABILIDADES ENCONTRADAS:")
        for i, vuln in enumerate(report['vulnerabilities'], 1):
            print(f"\n{i}. Rota: {vuln['method']} {vuln['path']}")
            for issue in vuln['issues']:
                print(f"   - {issue}")
    
    print("\nRECOMENDAÇÕES:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"{i}. {rec}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    # Executa a verificação e exibe o relatório
    print_security_report()

