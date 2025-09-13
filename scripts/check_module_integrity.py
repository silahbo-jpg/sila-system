#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar a integridade dos módulos do backend.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Cores para saída no terminal
class Colors:
    HEADER = '/033[95m'
    OKBLUE = '/033[94m'
    OKCYAN = '/033[96m'
    OKGREEN = '/033[92m'
    WARNING = '/033[93m'
    FAIL = '/033[91m'
    ENDC = '/033[0m'
    BOLD = '/033[1m'
    UNDERLINE = '/033[4m'

# Configurações
BASE_DIR = Path("backend/app/modules")
REQUIRED_FILES = [
    "__init__.py",
    "crud.py",
    "endpoints.py",
    "models.py",
    "schemas.py",
    "services.py"
]

def check_module(module_name: str) -> Tuple[bool, Dict[str, bool], List[str]]:
    """Verifica a integridade de um módulo."""
    module_path = BASE_DIR / module_name
    
    if not module_path.exists() or not module_path.is_dir():
        return False, {}, [f"O diretório do módulo {module_name} não existe."]
    
    missing_files = []
    files_status = {}
    
    for file in REQUIRED_FILES:
        file_path = module_path / file
        file_exists = file_path.exists() and file_path.is_file()
        files_status[file] = file_exists
        
        if not file_exists and file != "__init__.py":
            missing_files.append(f"Arquivo {file} não encontrado em {module_name}")
    
    return len(missing_files) == 0, files_status, missing_files

def check_imports(module_name: str) -> List[str]:
    """Verifica se há imports problemáticos no módulo."""
    module_path = BASE_DIR / module_name
    if not module_path.exists():
        return [f"Módulo {module_name} não encontrado"]
    
    issues = []
    
    # Verifica imports em cada arquivo do módulo
    for file in REQUIRED_FILES:
        if file == "__init__.py":
            continue
            
        file_path = module_path / file
        if not file_path.exists():
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Verifica referências ao módulo health
                if 'health' in content.lower() and 'health' not in content.lower():
                    issues.append(f"Possível referência ao módulo 'health' em {file_path}")
                    
        except Exception as e:
            issues.append(f"Erro ao ler o arquivo {file_path}: {str(e)}")
    
    return issues

def check_main_imports() -> List[str]:
    """Verifica se o módulo está corretamente importado no main.py."""
    main_path = Path("backend/app/main.py")
    if not main_path.exists():
        return ["Arquivo main.py não encontrado"]
    
    issues = []
    
    try:
        with open(main_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Verifica se o módulo health está corretamente importado
            if 'from app.modules.health.endpoints import router as health_router' not in content:
                issues.append("Importação do módulo health não encontrada no main.py")
                
            if 'app.include_router(health_router, prefix="/api")' not in content:
                issues.append("Registro do roteador do módulo health não encontrado no main.py")
                
    except Exception as e:
        issues.append(f"Erro ao ler o arquivo main.py: {str(e)}")
    
    return issues

def main():
    print(f"{Colors.HEADER}=== Verificador de Integridade de Módulos ==={Colors.ENDC}/n")
    
    # Verifica se o diretório base existe
    if not BASE_DIR.exists():
        print(f"{Colors.FAIL}Erro: Diretório não encontrado: {BASE_DIR.absolute()}{Colors.ENDC}")
        print("Certifique-se de que o script está sendo executado a partir do diretório raiz do projeto.")
        sys.exit(1)
    
    # Lista os módulos disponíveis
    modules = [d.name for d in BASE_DIR.iterdir() 
              if d.is_dir() and d.name != "__pycache__" and (d / "endpoints.py").exists()]
    
    if not modules:
        print(f"{Colors.WARNING}Nenhum módulo encontrado.{Colors.ENDC}")
        sys.exit(0)
    
    print(f"{Colors.OKBLUE}Verificando integridade dos módulos...{Colors.ENDC}/n")
    
    all_ok = True
    
    for module in sorted(modules):
        print(f"{Colors.BOLD}Módulo: {module}{Colors.ENDC}")
        
        # Verifica arquivos do módulo
        is_ok, files_status, issues = check_module(module)
        
        # Exibe status dos arquivos
        for file, exists in files_status.items():
            status = f"{Colors.OKGREEN}✓{Colors.ENDC}" if exists else f"{Colors.FAIL}✗{Colors.ENDC}"
            print(f"  {status} {file}")
        
        # Verifica imports problemáticos
        import_issues = check_imports(module)
        issues.extend(import_issues)
        
        # Exibe problemas encontrados
        if issues:
            all_ok = False
            print(f"/n{Colors.WARNING}Problemas encontrados:{Colors.ENDC}")
            for issue in issues:
                print(f"  • {issue}")
        else:
            print(f"{Colors.OKGREEN}✓ Módulo íntegro{Colors.ENDC}")
        
        print()
    
    # Verifica imports no main.py
    print(f"{Colors.BOLD}Verificando imports no main.py...{Colors.ENDC}")
    main_issues = check_main_imports()
    
    if main_issues:
        all_ok = False
        for issue in main_issues:
            print(f"  {Colors.FAIL}✗ {issue}{Colors.ENDC}")
    else:
        print(f"  {Colors.OKGREEN}✓ Imports no main.py estão corretos{Colors.ENDC}")
    
    print("/n" + "="*50 + "/n")
    
    if all_ok and not main_issues:
        print(f"{Colors.OKGREEN}✓ Todos os módulos estão íntegros!{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}Alguns problemas foram encontrados. Por favor, revise as mensagens acima.{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"/n{Colors.FAIL}Erro inesperado: {e}{Colors.ENDC}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

