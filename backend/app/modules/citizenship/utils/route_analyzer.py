"""
Script para analisar rotas do módulo de cidadania.

Este script analisa o arquivo de endpoints para verificar se as rotas estão
devidamente protegidas com autenticação e permissões.
"""
import re
import ast
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

# Padrões de regex para análise
decorator_pattern = re.compile(r'@router\.(get|post|put|delete|patch|head|options|trace)\s*\(\s*[\'"]([^\'")]+)[\'"]', re.IGNORECASE)
function_def_pattern = re.compile(r'def\s+(\w+)\s*\(')
depends_pattern = re.compile(r'Depends\(([^)]+)\)')
current_user_pattern = re.compile(r'current_user(_id)?\s*:')
permission_pattern = re.compile(r'require_\w+')

# Mapeamento de métodos HTTP para permissões esperadas
METHOD_TO_PERMISSION = {
    'GET': 'read',
    'POST': 'create',
    'PUT': 'update',
    'DELETE': 'delete',
    'PATCH': 'update',
    'HEAD': 'read',
    'OPTIONS': 'read',
    'TRACE': 'read'
}

# Mapeamento de rotas para permissões esperadas
ROUTE_PERMISSIONS = {
    # Rotas de cidadãos
    'POST /citizens/': 'citizenship:citizen:create',
    'GET /citizens/': 'citizenship:citizen:read',
    'GET /citizens/{citizen_id}': 'citizenship:citizen:read',
    'PUT /citizens/{citizen_id}': 'citizenship:citizen:update',
    'DELETE /citizens/{citizen_id}': 'citizenship:citizen:delete',
    
    # Rotas de documentos
    'POST /citizens/{citizen_id}/documents/': 'citizenship:document:upload',
    'GET /citizens/{citizen_id}/documents/': 'citizenship:document:read',
    'GET /documents/{document_id}/download': 'citizenship:document:download',
    'GET /documents/verify/{uuid}': 'citizenship:document:verify',
    'GET /documents/{document_id}/generate-pdf': 'citizenship:document:generate_pdf',
    
    # Rotas de membros da família
    'POST /citizens/{citizen_id}/family/': 'citizenship:family:add',
    'GET /citizens/{citizen_id}/family/': 'citizenship:family:view',
    'DELETE /family/{member_id}': 'citizenship:family:remove',
    
    # Rotas de feedback
    'POST /feedback/': 'citizenship:feedback:create',
    'GET /feedback/': 'citizenship:feedback:read',
    'GET /feedback/{feedback_id}': 'citizenship:feedback:read',
    'PATCH /feedback/{feedback_id}': 'citizenship:feedback:update',
    'DELETE /feedback/{feedback_id}': 'citizenship:feedback:delete',
}

# Mapeamento de permissões para descrições amigáveis
PERMISSION_DESCRIPTIONS = {
    'citizenship:citizen:create': 'Criar novos cidadãos',
    'citizenship:citizen:read': 'Visualizar informações de cidadãos',
    'citizenship:citizen:update': 'Atualizar informações de cidadãos',
    'citizenship:citizen:delete': 'Remover cidadãos (soft delete)',
    'citizenship:document:upload': 'Enviar documentos',
    'citizenship:document:read': 'Visualizar documentos',
    'citizenship:document:download': 'Baixar documentos',
    'citizenship:document:verify': 'Verificar documentos (público)',
    'citizenship:document:generate_pdf': 'Gerar PDF de documentos',
    'citizenship:family:add': 'Adicionar membros da família',
    'citizenship:family:view': 'Visualizar membros da família',
    'citizenship:family:remove': 'Remover membros da família',
    'citizenship:feedback:create': 'Criar feedback',
    'citizenship:feedback:read': 'Visualizar feedbacks',
    'citizenship:feedback:update': 'Atualizar feedbacks',
    'citizenship:feedback:delete': 'Excluir feedbacks',
}

# Mapeamento de permissões para níveis de acesso necessários
PERMISSION_ACCESS_LEVELS = {
    'citizenship:citizen:create': 'postgres',
    'citizenship:citizen:read': 'staff',
    'citizenship:citizen:update': 'staff',
    'citizenship:citizen:delete': 'postgres',
    'citizenship:document:upload': 'staff',
    'citizenship:document:read': 'staff',
    'citizenship:document:download': 'staff',
    'citizenship:document:verify': 'public',
    'citizenship:document:generate_pdf': 'staff',
    'citizenship:family:add': 'staff',
    'citizenship:family:view': 'staff',
    'citizenship:family:remove': 'staff',
    'citizenship:feedback:create': 'postgres',
    'citizenship:feedback:read': 'staff',
    'citizenship:feedback:update': 'staff',
    'citizenship:feedback:delete': 'postgres',
}

class RouteAnalysis:
    """Classe para armazenar a análise de uma rota."""
    
    def __init__(self, path: str, methods: List[str]):
        self.path = path
        self.methods = methods
        self.function_name = ""
        self.has_auth = False
        self.permissions: List[str] = []
        self.dependencies: List[str] = []
        self.line_number = 0
        self.required_permissions: List[str] = []
    
    def add_dependency(self, dep: str):
        """Adiciona uma dependência à rota."""
        dep = dep.strip()
        if 'current_user' in dep or 'get_current_active_user' in dep or 'get_current_user_id' in dep:
            self.has_auth = True
        if 'require_' in dep:
            self.permissions.append(dep)
        if dep not in self.dependencies:
            self.dependencies.append(dep)
    
    def is_secure(self) -> bool:
        """Verifica se a rota está adequadamente protegida."""
        # Rotas que não precisam de autenticação (ex: verificação de documento público)
        if 'verify' in self.path:
            return True
            
        # Verifica se tem autenticação e as permissões necessárias
        required_perms = self.get_required_permissions()
        if not required_perms:  # Se não há permissão definida, considera insegura
            return False
            
        # Verifica se tem todas as permissões necessárias
        has_all_perms = all(
            any(perm in req_perm for perm in self.permissions)
            for req_perm in required_perms
        )
        
        return self.has_auth and (has_all_perms or 'postgres' in self.dependencies)
    
    def get_required_permissions(self) -> List[str]:
        """Retorna as permissões necessárias para a rota, se definidas."""
        if self.required_permissions:
            return self.required_permissions
            
        perms = []
        for method in self.methods:
            key = f"{method} {self.path}"
            if key in ROUTE_PERMISSIONS:
                perm = ROUTE_PERMISSIONS[key]
                if perm not in perms:
                    perms.append(perm)
        
        self.required_permissions = perms
        return perms
    
    def get_issues(self) -> List[Dict[str, str]]:
        """Retorna uma lista de problemas de segurança encontrados na rota."""
        issues = []
        
        # Rotas de verificação são sempre consideradas seguras
        if 'verify' in self.path:
            return issues
        
        # Verifica autenticação
        if not self.has_auth:
            issues.append({
                'type': 'auth',
                'severity': 'high',
                'message': 'Falta autenticação (current_user não encontrado)',
                'solution': 'Adicione Depends(get_current_active_user) à assinatura da função'
            })
        
        # Verifica permissões necessárias
        required_perms = self.get_required_permissions()
        if not required_perms:
            issues.append({
                'type': 'permission',
                'severity': 'medium',
                'message': 'Nenhuma permissão definida para esta rota',
                'solution': 'Defina as permissões necessárias em ROUTE_PERMISSIONS e adicione as dependências correspondentes'
            })
        else:
            for req_perm in required_perms:
                if not any(perm in req_perm for perm in self.permissions):
                    access_level = PERMISSION_ACCESS_LEVELS.get(req_perm, 'desconhecido')
                    issues.append({
                        'type': 'permission',
                        'severity': 'high' if access_level in ['postgres', 'staff'] else 'medium',
                        'message': f'Falta verificação de permissão: {req_perm} ({PERMISSION_DESCRIPTIONS.get(req_perm, "Sem descrição")})',
                        'solution': f'Adicione a dependência require_{req_perm.replace(":", "_")} ou verifique se o usuário tem a role {access_level}'
                    })
        
        return issues

def analyze_endpoints_file(file_path: str) -> Dict[str, RouteAnalysis]:
    """Analisa um arquivo de endpoints e retorna um dicionário com as rotas analisadas."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontra todas as funções de rota
    functions = []
    # Padrão para encontrar decoradores de rota como @router.get("/path")
    route_pattern = r'@router\.(get|post|put|delete|patch|head|options|trace)\s*\(\s*["\']([^"\')]+)["\']'
    
    for match in re.finditer(route_pattern, content, re.IGNORECASE):
        method = match.group(1).upper()
        path = match.group(2).strip()
        
        # Encontra o nome da função após o decorador
        remaining_content = content[match.end():]
        func_match = re.search(r'def\s+(\w+)\s*\(', remaining_content)
        
        if func_match:
            func_name = func_match.group(1)
            # Encontra a posição do início da função
            func_pos = match.end() + func_match.start()
            functions.append((method, path, func_name, func_pos))
            print(f"Encontrada rota: {method} {path} -> {func_name} (pos: {func_pos})")
    
    # Ordena as funções pela posição no arquivo
    functions.sort(key=lambda x: x[3])
    
    # Encontra as dependências de cada função
    routes: Dict[str, RouteAnalysis] = {}
    
    for i, (method, path, func_name, pos) in enumerate(functions):
        # Encontra o final da função (próxima função ou fim do arquivo)
        next_pos = functions[i+1][3] if i+1 < len(functions) else len(content)
        func_content = content[pos:next_pos]
        
        # Remove comentários para evitar falsos positivos
        func_content_no_comments = re.sub(r'#.*?$', '', func_content, flags=re.MULTILINE)
        
        # Cria ou atualiza a análise da rota
        route_key = f"{method} {path}"
        if route_key not in routes:
            routes[route_key] = RouteAnalysis(path, [method])
        else:
            routes[route_key].methods.append(method)
        
        route = routes[route_key]
        route.function_name = func_name
        
        # Encontra as dependências na assinatura da função
        func_decl = func_content.split(':', 1)[0]
        for dep_match in depends_pattern.finditer(func_decl):
            dep = dep_match.group(1).strip()
            # Extrai o nome da dependência (remove chamadas de função)
            dep_name = dep.split('(')[0].strip()
            route.add_dependency(dep_name)
        
        # Verifica se há autenticação nas dependências
        if any(dep in ['get_current_active_user', 'get_current_user_id'] for dep in route.dependencies):
            route.has_auth = True
        # Verifica se há autenticação no corpo da função
        elif 'current_user' in func_content_no_comments:
            # Verifica se não é uma atribuição ou uso em uma condição
            if not re.search(r'current_user\s*=', func_content_no_comments) and \
               not re.search(r'if\s+\(?=.*current_user\)', func_content_no_comments):
                route.has_auth = True
    
    return routes

def generate_security_report(file_path: str) -> Dict[str, any]:
    """Gera um relatório de segurança para as rotas do arquivo de endpoints."""
    routes = analyze_endpoints_file(file_path)
    
    # Contadores para o relatório
    total_routes = len(routes)
    secure_routes = 0
    vulnerabilities = []
    auth_issues = 0
    permission_issues = 0
    
    # Analisa as rotas
    for path, route in routes.items():
        if route.is_secure():
            secure_routes += 1
        else:
            for method in route.methods:
                issues = route.get_issues()
                if issues:
                    for issue in issues:
                        if issue['type'] == 'auth':
                            auth_issues += 1
                        elif issue['type'] == 'permission':
                            permission_issues += 1
                    
                    vulnerabilities.append({
                        'method': method,
                        'path': path,
                        'function': route.function_name,
                        'issues': issues,
                        'required_permissions': route.get_required_permissions(),
                        'current_permissions': route.permissions,
                        'dependencies': route.dependencies
                    })
    
    # Gera estatísticas
    security_score = (secure_routes / total_routes * 100) if total_routes > 0 else 0
    
    # Gera recomendações baseadas nas vulnerabilidades encontradas
    recommendations = []
    if auth_issues > 0:
        recommendations.append({
            'priority': 'high',
            'description': f'Adicionar autenticação em {auth_issues} rotas',
            'action': 'Certifique-se de que todas as rotas que manipulam dados sensíveis usem Depends(get_current_active_user) ou Depends(get_current_user_id)'
        })
    
    if permission_issues > 0:
        recommendations.append({
            'priority': 'high' if permission_issues > 5 else 'medium',
            'description': f'Corrigir {permission_issues} problemas de permissão',
            'action': 'Adicione as dependências de permissão necessárias (require_*) a cada rota'
        })
    
    # Adiciona recomendações gerais
    recommendations.extend([
        {
            'priority': 'medium',
            'description': 'Implementar verificação de autorização baseada em papéis (RBAC)',
            'action': 'Use as permissões definidas em PERMISSION_ACCESS_LEVELS para implementar verificações de autorização'
        },
        {
            'priority': 'low',
            'description': 'Documentar as permissões necessárias',
            'action': 'Atualize as docstrings das rotas para incluir as permissões necessárias'
        },
        {
            'priority': 'medium',
            'description': 'Adicionar testes de segurança',
            'action': 'Crie testes automatizados para verificar as permissões de cada rota'
        }
    ])
    
    # Gera o relatório
    report = {
        'module': 'citizenship',
        'file_analyzed': file_path,
        'timestamp': datetime.now().isoformat(),
        'statistics': {
            'total_routes': total_routes,
            'secure_routes': secure_routes,
            'insecure_routes': total_routes - secure_routes,
            'security_score': f"{security_score:.1f}%",
            'auth_issues': auth_issues,
            'permission_issues': permission_issues,
        },
        'vulnerabilities': vulnerabilities,
        'recommendations': recommendations,
        'permission_reference': {
            'available_permissions': list(PERMISSION_DESCRIPTIONS.keys()),
            'access_levels': sorted(set(PERMISSION_ACCESS_LEVELS.values()))
        }
    }
    
    return report

def print_security_report(file_path: str):
    """Imprime um relatório de segurança formatado para o arquivo de endpoints."""
    from textwrap import fill
    from datetime import datetime
    
    report = generate_security_report(file_path)
    
    # Cores para o terminal
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    def print_section(title: str, char: str = '='):
        """Imprime um título de seção formatado."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{title.center(80, ' ')}{Colors.ENDC}")
        print(char * 80)
    
    def print_issue(issue: dict, indent: int = 0):
        """Imprime um problema de segurança formatado."""
        prefix = '  ' * indent
        severity_color = {
            'high': Colors.FAIL,
            'medium': Colors.WARNING,
            'low': Colors.OKCYAN
        }.get(issue.get('severity', 'medium'), Colors.WARNING)
        
        print(f"{prefix}{severity_color}● {issue['message']}{Colors.ENDC}")
        print(f"{prefix}  {Colors.OKBLUE}Solução:{Colors.ENDC} {issue['solution']}")
    
    # Cabeçalho do relatório
    print("\n" + "=" * 80)
    print(f"{Colors.HEADER}{Colors.BOLD}{'RELATÓRIO DE SEGURANÇA - MÓDULO CITIZENSHIP':^80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
    print(f"Arquivo analisado: {Colors.OKBLUE}{report['file_analyzed']}{Colors.ENDC}")
    print(f"Data da análise: {datetime.fromisoformat(report['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Estatísticas
    print_section("ESTATÍSTICAS")
    stats = report['statistics']
    security_score = float(stats['security_score'].rstrip('%'))
    score_color = Colors.OKGREEN if security_score > 80 else Colors.WARNING if security_score > 50 else Colors.FAIL
    
    print(f"Total de rotas analisadas: {Colors.BOLD}{stats['total_routes']}{Colors.ENDC}")
    print(f"Rotas seguras: {Colors.OKGREEN}{stats['secure_routes']}{Colors.ENDC}")
    print(f"Rotas com problemas: {Colors.FAIL if stats['insecure_routes'] > 0 else Colors.OKGREEN}{stats['insecure_routes']}{Colors.ENDC}")
    print(f"Pontuação de segurança: {score_color}{stats['security_score']}{Colors.ENDC}")
    print(f"Problemas de autenticação: {Colors.FAIL if stats['auth_issues'] > 0 else Colors.OKGREEN}{stats['auth_issues']}{Colors.ENDC}")
    print(f"Problemas de permissão: {Colors.WARNING if stats['permission_issues'] > 0 else Colors.OKGREEN}{stats['permission_issues']}{Colors.ENDC}")
    
    # Vulnerabilidades
    if report['vulnerabilities']:
        print_section("VULNERABILIDADES ENCONTRADAS", '-')
        for i, vuln in enumerate(report['vulnerabilities'], 1):
            print(f"\n{Colors.BOLD}{i}. {vuln['method']} {vuln['path']}{Colors.ENDC} ({Colors.OKBLUE}{vuln['function']}{Colors.ENDC})")
            
            # Mostra permissões necessárias vs atuais
            if vuln['required_permissions']:
                print(f"  {Colors.OKBLUE}Permissões necessárias:{Colors.ENDC}")
                for perm in vuln['required_permissions']:
                    desc = PERMISSION_DESCRIPTIONS.get(perm, "Sem descrição")
                    level = PERMISSION_ACCESS_LEVELS.get(perm, "desconhecido")
                    print(f"    - {perm} ({desc}) [Nível: {level}]")
            
            # Mostra permissões atuais
            if vuln['current_permissions']:
                print(f"  {Colors.OKGREEN}Permissões atuais:{Colors.ENDC}")
                for perm in set(vuln['current_permissions']):
                    print(f"    - {perm}")
            else:
                print(f"  {Colors.FAIL}Nenhuma permissão definida{Colors.ENDC}")
            
            # Mostra problemas
            print(f"  {Colors.WARNING}Problemas encontrados:{Colors.ENDC}")
            for issue in vuln['issues']:
                print_issue(issue, indent=2)
    
    # Recomendações
    if report['recommendations']:
        print_section("RECOMENDAÇÕES", '-')
        for i, rec in enumerate(report['recommendations'], 1):
            priority_color = {
                'high': Colors.FAIL,
                'medium': Colors.WARNING,
                'low': Colors.OKCYAN
            }.get(rec['priority'], Colors.ENDC)
            
            print(f"\n{Colors.BOLD}{i}. {rec['description']}{Colors.ENDC} [{priority_color}{rec['priority'].upper()}{Colors.ENDC}]")
            print(f"   {rec['action']}")
    
    # Referência de permissões
    print_section("REFERÊNCIA DE PERMISSÕES", '-')
    print(f"{Colors.OKBLUE}Níveis de acesso disponíveis:{Colors.ENDC} {', '.join(report['permission_reference']['access_levels'])}")
    print(f"{Colors.OKBLUE}Permissões definidas:{Colors.ENDC}")
    
    # Agrupa permissões por domínio
    permissions_by_domain = {}
    for perm in report['permission_reference']['available_permissions']:
        domain = perm.split(':')[0]
        if domain not in permissions_by_domain:
            permissions_by_domain[domain] = []
        permissions_by_domain[domain].append(perm)
    
    for domain, perms in permissions_by_domain.items():
        print(f"\n  {Colors.BOLD}{domain.upper()}{Colors.ENDC}")
        for perm in sorted(perms):
            desc = PERMISSION_DESCRIPTIONS.get(perm, "")
            level = PERMISSION_ACCESS_LEVELS.get(perm, "")
            print(f"    - {perm:<40} {desc:<50} [Nível: {level}]")
    
    # Rodapé
    print("\n" + "=" * 80)
    print(f"{Colors.HEADER}{'ANÁLISE CONCLUÍDA':^80}{Colors.ENDC}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    import os
    
    # Caminho para o arquivo de endpoints
    current_dir = os.path.dirname(os.path.abspath(__file__))
    endpoints_file = os.path.join(current_dir, '..', 'endpoints.py')
    
    # Executa a análise e exibe o relatório
    print_security_report(endpoints_file)

