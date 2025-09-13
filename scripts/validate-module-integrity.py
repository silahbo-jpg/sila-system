#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de Integridade de Módulos do sila_dev

Este script consolida várias verificações de integridade em uma única ferramenta:
- Validação de sintaxe Python (usando py_compile)
- Verificação de padrões proibidos (SQLAlchemy, etc.)
- Verificação da estrutura de módulos e arquivos __init__.py
- Geração de relatórios detalhados
"""

import os
import sys
import ast
import py_compile
import re
import time
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# Configurações
PROJECT_sila_dev-system = Path(__file__).parent.parent
BACKEND = PROJECT_sila_dev-system / "backend"
MODULES_PATH = BACKEND / "app" / "modules"

# Configuração de logging
log_dir = PROJECT_sila_dev-system / "logs"
log_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = log_dir / f"module_integrity_{timestamp}.log"

# Arquivo de relatório
report_dir = PROJECT_sila_dev-system / "reports"
report_dir.mkdir(exist_ok=True)
report_file = report_dir / f"module_integrity_{timestamp}.md"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Padrões proibidos (pós-migração para Prisma)
FORBIDDEN_PATTERNS = [
    ("from sqlalchemy", "Use Prisma, não SQLAlchemy"),
    ("import sqlalchemy", "Use Prisma, não SQLAlchemy"),
    ("SessionLocal", "ORM antigo removido, use get_db"),
    ("Base.metadata", "Migração para Prisma concluída"),
    ("create_engine", "Banco gerenciado por Prisma"),
    ("declarative_base", "Não usar SQLAlchemy"),
]

# Módulos que devem ter __init__.py
MODULES_EXPECTING_INIT = [
    "app/core",
    "app/db",
    "app/api/routes",
    "app/middleware",
    "app/services",
    "app/schemas",
    "app/modules",
]

# Arquivos obrigatórios para cada módulo
REQUIRED_FILES = [
    "__init__.py", 
    "models.py", 
    "schemas.py", 
    "crud.py", 
    "services.py", 
    "endpoints.py"
]


class Severity(str, Enum):
    """Níveis de severidade para problemas encontrados."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class CheckResult:
    """Resultado de uma verificação individual."""
    name: str
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed: bool
    severity: Severity
    details: str = ""
    fix_suggestion: str = ""


@dataclass
class ValidationResult:
    """Resultado da validação de um módulo ou arquivo."""
    name: str
    checks: List[CheckResult] = field(default_factory=list)
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


def check_syntax(file_path: Path) -> Tuple[bool, str]:
    """Verifica a sintaxe de um arquivo Python usando py_compile.
    
    Args:
        file_path: Caminho do arquivo a ser validado
        
    Returns:
        Tupla (sucesso, mensagem_erro)
    """
    try:
        py_compile.compile(str(file_path), doraise=True)
        return True, ""
    except Exception as e:
        return False, str(e)


def find_python_files(sila_dev-system_dir: Path, ignore_dirs: Optional[List[str]] = None) -> List[Path]:
    """Encontra todos os arquivos Python em um diretório recursivamente.
    
    Args:
        sila_dev-system_dir: Diretório raiz para iniciar a busca
        ignore_dirs: Lista de diretórios a serem ignorados
        
    Returns:
        Lista de caminhos de arquivos Python
    """
    if ignore_dirs is None:
        ignore_dirs = ['archived', 'venv', '.venv', 'env', '.env', '__pycache__', 'node_modules', '.git']
    
    python_files = []
    
    for path in sila_dev-system_dir.rglob("*.py"):
        # Verifica se o arquivo está em um diretório ignorado
        if any(ignore_dir in path.parts for ignore_dir in ignore_dirs):
            continue
        python_files.append(path)
                
    return python_files


def check_forbidden_patterns(file_path: Path) -> List[Tuple[str, str, int]]:
    """Verifica padrões proibidos em um arquivo.
    
    Args:
        file_path: Caminho do arquivo a ser verificado
        
    Returns:
        Lista de tuplas (padrão, mensagem, linha)
    """
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
            for i, line in enumerate(lines):
                for pattern, message in FORBIDDEN_PATTERNS:
                    if pattern in line and not line.strip().startswith('#'):
                        issues.append((pattern, message, i + 1))
    except Exception as e:
        logger.error(f"Erro ao verificar padrões em {file_path}: {e}")
    
    return issues


def check_init_files() -> List[str]:
    """Verifica se todos os diretórios que devem ter __init__.py os têm.
    
    Returns:
        Lista de diretórios sem __init__.py
    """
    missing_init = []
    
    for module_path in MODULES_EXPECTING_INIT:
        full_path = BACKEND / Path(module_path)
        init_file = full_path / "__init__.py"
        
        if full_path.exists() and full_path.is_dir() and not init_file.exists():
            missing_init.append(module_path)
    
    # Verifica também todos os subdiretórios em app/modules
    modules_dir = BACKEND / "app" / "modules"
    if modules_dir.exists():
        for module_dir in modules_dir.iterdir():
            if module_dir.is_dir() and not module_dir.name.startswith('__'):
                init_file = module_dir / "__init__.py"
                if not init_file.exists():
                    missing_init.append(f"app/modules/{module_dir.name}")
    
    return missing_init


def check_module_structure(module_name: str) -> Tuple[bool, Dict[str, bool], List[str]]:
    """Verifica a estrutura de um módulo.
    
    Args:
        module_name: Nome do módulo a ser verificado
        
    Returns:
        Tupla (sucesso, status_arquivos, problemas)
    """
    module_path = MODULES_PATH / module_name
    
    if not module_path.exists() or not module_path.is_dir():
        return False, {}, [f"O diretório do módulo {module_name} não existe."]
    
    missing_files = []
    files_status = {}
    
    for file in REQUIRED_FILES:
        file_path = module_path / file
        file_exists = file_path.exists() and file_path.is_file()
        files_status[file] = file_exists
        
        if not file_exists:
            missing_files.append(f"Arquivo {file} não encontrado em {module_name}")
    
    return len(missing_files) == 0, files_status, missing_files


def validate_modules() -> Dict[str, ValidationResult]:
    """Valida todos os módulos do sistema.
    
    Returns:
        Dicionário com os resultados da validação
    """
    results = {}
    
    if not MODULES_PATH.exists():
        logger.error(f"Diretório de módulos não encontrado: {MODULES_PATH}")
        return results
    
    # Lista todos os módulos
    modules = [d.name for d in MODULES_PATH.iterdir() 
              if d.is_dir() and not d.name.startswith('__')]
    
    for module_name in sorted(modules):
        result = ValidationResult(name=module_name)
        
        # Verifica estrutura do módulo
        is_ok, files_status, issues = check_module_structure(module_name)
        
        # Adiciona resultados das verificações de arquivos
        for file, exists in files_status.items():
            severity = Severity.HIGH if file != "__init__.py" else Severity.MEDIUM
            check = CheckResult(
                name=f"Arquivo {file} existe",
                Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=exists,
                severity=severity,
                details="" if exists else f"Arquivo {file} não encontrado",
                fix_suggestion="" if exists else f"Crie o arquivo {file} no módulo {module_name}"
            )
            result.checks.append(check)
        
        # Verifica sintaxe dos arquivos Python
        module_path = MODULES_PATH / module_name
        for file_path in module_path.glob("*.py"):
            syntax_ok, error_msg = check_syntax(file_path)
            check = CheckResult(
                name=f"Sintaxe válida em {file_path.name}",
                Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=syntax_ok,
                severity=Severity.HIGH,
                details="" if syntax_ok else f"Erro de sintaxe: {error_msg}",
                fix_suggestion="" if syntax_ok else "Corrija os erros de sintaxe no arquivo"
            )
            result.checks.append(check)
        
        # Verifica padrões proibidos
        for file_path in module_path.glob("*.py"):
            issues = check_forbidden_patterns(file_path)
            if issues:
                patterns = ", ".join(set(issue[0] for issue in issues))
                lines = ", ".join(str(issue[2]) for issue in issues)
                check = CheckResult(
                    name=f"Sem padrões proibidos em {file_path.name}",
                    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=False,
                    severity=Severity.HIGH,
                    details=f"Padrões proibidos encontrados: {patterns} nas linhas {lines}",
                    fix_suggestion="Execute scripts/fix-sqlalchemy-refs.py para corrigir automaticamente"
                )
                result.checks.append(check)
            else:
                check = CheckResult(
                    name=f"Sem padrões proibidos em {file_path.name}",
                    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed=True,
                    severity=Severity.HIGH
                )
                result.checks.append(check)
        
        # Atualiza status geral do módulo
        result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed = all(check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed for check in result.checks)
        results[module_name] = result
    
    return results


def generate_markdown_report(results: Dict[str, ValidationResult], missing_init: List[str]) -> str:
    """Gera um relatório em formato Markdown.
    
    Args:
        results: Resultados da validação de módulos
        missing_init: Lista de diretórios sem __init__.py
        
    Returns:
        Relatório em formato Markdown
    """
    report = []
    report.append("# Relatório de Validação de Integridade de Módulos")
    report.append(f"\nData: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Resumo
    total_modules = len(results)
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules = sum(1 for result in results.values() if result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed)
    
    report.append("## Resumo")
    report.append(f"- Total de módulos: {total_modules}")
    report.append(f"- Módulos válidos: {Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules}")
    report.append(f"- Módulos com problemas: {total_modules - Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules}")
    
    # Verificação de __init__.py
    report.append("\n## Verificação de arquivos __init__.py")
    if missing_init:
        report.append("\n❌ **Diretórios sem __init__.py:**")
        for path in missing_init:
            report.append(f"- `{path}`")
        report.append("\n**Sugestão:** Crie os arquivos __init__.py nos diretórios listados acima.")
    else:
        report.append("\n✅ Todos os diretórios necessários possuem arquivos __init__.py.")
    
    # Detalhes por módulo
    report.append("\n## Detalhes por Módulo")
    
    for module_name, result in sorted(results.items()):
        status = "✅" if result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed else "❌"
        report.append(f"\n### {status} Módulo: {module_name}")
        
        # Agrupa verificações por tipo
        structure_checks = []
        syntax_checks = []
        pattern_checks = []
        
        for check in result.checks:
            if "existe" in check.name:
                structure_checks.append(check)
            elif "Sintaxe" in check.name:
                syntax_checks.append(check)
            elif "padrões proibidos" in check.name:
                pattern_checks.append(check)
        
        # Estrutura de arquivos
        report.append("\n#### Estrutura de Arquivos")
        for check in structure_checks:
            status = "✅" if check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed else "❌"
            report.append(f"- {status} {check.name}")
            if not check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed and check.fix_suggestion:
                report.append(f"  - *Sugestão:* {check.fix_suggestion}")
        
        # Sintaxe
        if syntax_checks:
            report.append("\n#### Sintaxe Python")
            failed_syntax = [check for check in syntax_checks if not check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed]
            if failed_syntax:
                for check in failed_syntax:
                    report.append(f"- ❌ {check.name}")
                    report.append(f"  - *Erro:* {check.details}")
                    if check.fix_suggestion:
                        report.append(f"  - *Sugestão:* {check.fix_suggestion}")
            else:
                report.append("- ✅ Todos os arquivos têm sintaxe válida")
        
        # Padrões proibidos
        if pattern_checks:
            report.append("\n#### Padrões Proibidos")
            failed_patterns = [check for check in pattern_checks if not check.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed]
            if failed_patterns:
                for check in failed_patterns:
                    report.append(f"- ❌ {check.name}")
                    report.append(f"  - *Detalhes:* {check.details}")
                    if check.fix_suggestion:
                        report.append(f"  - *Sugestão:* {check.fix_suggestion}")
            else:
                report.append("- ✅ Nenhum padrão proibido encontrado")
    
    # Próximos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*os
    report.append("\n## Próximos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*os")
    
    if total_modules == Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules and not missing_init:
        report.append("\n✅ **Todos os módulos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*aram na validação!**")
        report.append("\nO sistema está pronto para execução.")
    else:
        report.append("\n1. **Corrija os problemas identificados:**")
        if missing_init:
            report.append("   - Crie os arquivos __init__.py nos diretórios listados")
        
        failed_modules = [name for name, result in results.items() if not result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed]
        if failed_modules:
            report.append("   - Resolva os problemas nos seguintes módulos: " + ", ".join(failed_modules))
        
        report.append("\n2. **Execute novamente este validador para confirmar as correções.**")
        report.append("\n3. **Após todas as correções, o sistema estará pronto para execução.**")
    
    return "\n".join(report)


def main():
    """Função principal que executa todas as validações."""
    start_time = time.time()
    
    logger.info("Iniciando validação de integridade de módulos...")
    
    # Verifica arquivos __init__.py
    logger.info("Verificando arquivos __init__.py...")
    missing_init = check_init_files()
    if missing_init:
        logger.warning(f"Encontrados {len(missing_init)} diretórios sem __init__.py")
        for path in missing_init:
            logger.warning(f"  - {path}")
    else:
        logger.info("Todos os diretórios necessários possuem arquivos __init__.py")
    
    # Valida módulos
    logger.info("Validando módulos...")
    results = validate_modules()
    
    # Gera relatório
    logger.info("Gerando relatório...")
    report_content = generate_markdown_report(results, missing_init)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    # Calcula estatísticas
    total_modules = len(results)
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules = sum(1 for result in results.values() if result.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed)
    failed_modules = total_modules - Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules
    
    # Exibe resumo
    execution_time = time.time() - start_time
    logger.info("="*80)
    logger.info("RESUMO DA VALIDAÇÃO:")
    logger.info(f"Total de módulos: {total_modules}")
    logger.info(f"Módulos válidos: {Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed_modules}")
    logger.info(f"Módulos com problemas: {failed_modules}")
    logger.info(f"Diretórios sem __init__.py: {len(missing_init)}")
    logger.info(f"Tempo total de execução: {execution_time:.2f} segundos")
    logger.info(f"Relatório gerado em: {report_file}")
    
    # Determina o código de saída
    if failed_modules > 0 or missing_init:
        logger.error("\n❌ Validação falhou! Existem problemas que precisam ser corrigidos.")
        return 1
    else:
        logger.info("\n✅ Validação concluída com sucesso! Todos os módulos estão íntegros.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

