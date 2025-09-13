#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e preencher automaticamente módulos que estão faltando componentes.
Baseado na estrutura do módulo 'citizenship' como referência.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

# Configurações
BASE_DIR = Path("backend/app/modules")
TEMPLATE_MODULE = "citizenship"  # Módulo a ser usado como referência
REQUIRED_FILES = ["crud.py", "endpoints.py", "models.py", "schemas.py", "services.py"]
EXCLUDE_DIRS = ["__pycache__"]

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

def get_module_name(module_path: Path) -> str:
    """Extrai o nome do módulo a partir do caminho."""
    return module_path.name

def get_module_files(module_path: Path) -> Dict[str, bool]:
    """Verifica quais arquivos obrigatórios existem no módulo."""
    return {filename: (module_path / filename).exists() for filename in REQUIRED_FILES}

def analyze_modules() -> Dict[str, Dict[str, bool]]:
    """Analisa todos os módulos e verifica arquivos faltantes."""
    modules_status = {}
    
    for module_dir in sorted(BASE_DIR.iterdir()):
        if not module_dir.is_dir() or module_dir.name in EXCLUDE_DIRS:
            continue
            
        module_name = get_module_name(module_dir)
        modules_status[module_name] = get_module_files(module_dir)
    
    return modules_status

def generate_file_content(template_path: Path, module_name: str) -> str:
    """Gera o conteúdo de um novo arquivo baseado no template, substituindo nomes."""
    if not template_path.exists():
        return ""
    
    content = template_path.read_text(encoding='utf-8')
    
    # Substitui referências ao nome do módulo template pelo novo módulo
    module_class = module_name.capitalize()
    content = content.replace("citizenship", module_name)
    content = content.replace("Citizenship", module_class)
    content = content.replace("CITIZENSHIP", module_name.upper())
    
    # Ajusta imports e referências específicas
    content = re.sub(
        r'from /. import (/w+) as /w+',
        f'from . import //1 as {module_name}_//1',
        content
    )
    
    return content

def create_missing_files(module_name: str, template_module: str, missing_files: List[str]) -> None:
    """Cria os arquivos ausentes no módulo com base no template."""
    module_path = BASE_DIR / module_name
    template_path = BASE_DIR / template_module
    
    for filename in missing_files:
        template_file = template_path / filename
        new_file = module_path / filename
        
        if not template_file.exists():
            print(f"{Colors.WARNING}Aviso: Arquivo template não encontrado: {template_file}{Colors.ENDC}")
            continue
            
        content = generate_file_content(template_file, module_name)
        
        # Cria o diretório se não existir
        new_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Escreve o novo arquivo
        new_file.write_text(content, encoding='utf-8')
        print(f"{Colors.OKGREEN}Criado: {new_file.relative_to(BASE_DIR.parent)}{Colors.ENDC}")

def generate_module_report(modules_status: Dict[str, Dict[str, bool]]) -> str:
    """Gera um relatório em markdown com o status dos módulos."""
    report = "# Relatório de Módulos/n/n"
    report += "| Módulo | " + " | ".join(REQUIRED_FILES) + " | Status |/n"
    report += "|--------|" + "| ".join(["------"] * len(REQUIRED_FILES)) + "|--------|/n"
    
    for module, files in modules_status.items():
        status_icons = []
        for filename in REQUIRED_FILES:
            status_icons.append("✅" if files.get(filename, False) else "❌")
        
        status = "✅ Completo" if all(files.values()) else "⚠️ Incompleto"
        report += f"| {module} | " + " | ".join(status_icons) + f" | {status} |/n"
    
    return report

def ensure_directory_exists(directory: Path) -> None:
    """Garante que o diretório existe, criando-o se necessário."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"{Colors.FAIL}Erro ao criar diretório {directory}: {e}{Colors.ENDC}")
        sys.exit(1)

def main():
    print(f"{Colors.HEADER}=== Verificador e Gerador de Módulos ==={Colors.ENDC}/n")
    
    # Verifica se o diretório base existe
    if not BASE_DIR.exists():
        print(f"{Colors.FAIL}Erro: Diretório não encontrado: {BASE_DIR.absolute()}{Colors.ENDC}")
        print("Certifique-se de que o script está sendo executado a partir do diretório raiz do projeto.")
        sys.exit(1)
    
    # Verifica se o módulo template existe
    template_path = BASE_DIR / TEMPLATE_MODULE
    if not template_path.exists():
        print(f"{Colors.FAIL}Erro: Módulo template não encontrado: {template_path.absolute()}{Colors.ENDC}")
        sys.exit(1)
    
    # Analisa os módulos
    print(f"{Colors.OKBLUE}Analisando módulos em {BASE_DIR.absolute()}...{Colors.ENDC}")
    modules_status = analyze_modules()
    
    # Gera e exibe o relatório
    report = generate_module_report(modules_status)
    print("/n" + report)
    
    # Verifica se há módulos para atualizar
    needs_update = any(not all(files.values()) for module, files in modules_status.items() 
                      if module != TEMPLATE_MODULE)
    
    if not needs_update:
        print(f"{Colors.OKGREEN}Todos os módulos estão completos!{Colors.ENDC}")
        sys.exit(0)
    
    # Pergunta ao usuário se deseja preencher os módulos faltantes
    while True:
        try:
            response = input("/nDeseja preencher automaticamente os módulos com arquivos faltantes? (s/n): ").strip().lower()
            if response in ['s', 'n']:
                break
        except (KeyboardInterrupt, EOFError):
            print("/nOperação cancelada pelo usuário.")
            sys.exit(0)
    
    if response == 'n':
        print("Operação cancelada pelo usuário.")
        sys.exit(0)
    
    # Cria os arquivos faltantes
    print("/nCriando arquivos faltantes...")
    updated_modules = 0
    
    for module, files in modules_status.items():
        if module == TEMPLATE_MODULE:
            continue
            
        missing_files = [f for f, exists in files.items() if not exists]
        if missing_files:
            print(f"/n{Colors.BOLD}Módulo: {module}{Colors.ENDC}")
            create_missing_files(module, TEMPLATE_MODULE, missing_files)
            updated_modules += 1
    
    if updated_modules > 0:
        print(f"/n{Colors.OKGREEN}✓ Processo concluído! {updated_modules} módulos foram atualizados.{Colors.ENDC}")
    else:
        print(f"{Colors.OKBLUE}Nenhum módulo precisou ser atualizado.{Colors.ENDC}")
    
    # Salva o relatório em um arquivo
    report_dir = BASE_DIR.parent.parent / "docs"
    ensure_directory_exists(report_dir)
    
    report_path = report_dir / "estado_atual_reestruturacao.md"
    try:
        report_path.write_text(report, encoding='utf-8')
        print(f"/nRelatório salvo em: {report_path.absolute()}")
    except Exception as e:
        print(f"{Colors.WARNING}Erro ao salvar relatório: {e}{Colors.ENDC}")

def run():
    try:
        main()
    except Exception as e:
        print(f"/n{Colors.FAIL}Erro inesperado: {e}{Colors.ENDC}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run()

