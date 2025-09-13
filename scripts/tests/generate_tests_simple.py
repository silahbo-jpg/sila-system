#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para gerar testes básicos para os módulos do backend.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Configurações
BASE_DIR = Path("backend/app/modules")
TESTS_DIR = Path("tests/modules")

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

def get_test_content(module_name: str, class_name: str) -> str:
    """Gera o conteúdo do arquivo de teste para um módulo."""
    return f'''# -*- coding: utf-8 -*-
"""Testes para o módulo {module_name}."""

import pytest
from fastapi import status
from httpx import AsyncClient

# Testes para o endpoint raiz
@pytest.mark.asyncio
async def test_read_main(async_client: AsyncClient):
    """Testa o endpoint raiz do módulo {module_name}."""
    response = await async_client.get(f"/api/{module_name}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {{"message": "{module_name} module"}}

# Testes CRUD para {class_name}
@pytest.mark.asyncio
async def test_create_{module_name}(async_client: AsyncClient):
    """Testa a criação de um(a) {module_name}."""
    test_data = {{
        "name": "Test {class_name}",
    }}
    
    response = await async_client.post(
        f"/api/{module_name}/",
        json=test_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["name"] == test_data["name"]
    return data["id"]

@pytest.mark.asyncio
async def test_read_{module_name}(async_client: AsyncClient, test_id: int):
    """Testa a leitura de um(a) {module_name} por ID."""
    response = await async_client.get(f"/api/{module_name}/{{test_id}}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_id

@pytest.mark.asyncio
async def test_update_{module_name}(async_client: AsyncClient, test_id: int):
    """Testa a atualização de um(a) {module_name}."""
    update_data = {{
        "name": "Updated {class_name}",
    }}
    
    response = await async_client.put(
        f"/api/{module_name}/{{test_id}}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]

@pytest.mark.asyncio
async def test_delete_{module_name}(async_client: AsyncClient, test_id: int):
    """Testa a exclusão de um(a) {module_name}."""
    response = await async_client.delete(f"/api/{module_name}/{{test_id}}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verifica se o registro foi realmente excluído
    response = await async_client.get(f"/api/{module_name}/{{test_id}}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
'''

def get_conftest_content(module_name: str, class_name: str) -> str:
    """Gera o conteúdo do arquivo de configuração de testes."""
    return f'''# -*- coding: utf-8 -*-
"""Configuração de testes para o módulo {module_name}."""

import pytest
from fastapi import status
from httpx import AsyncClient

@pytest.fixture
def test_data():
    """Dados de teste para {module_name}."""
    return {{
        "name": "Test {class_name}",
    }}

@pytest.fixture
async def test_id(async_client: AsyncClient, test_data):
    """Cria um(a) {module_name} para teste e retorna o ID."""
    response = await async_client.post(
        f"/api/{module_name}/",
        json=test_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    return data["id"]
'''

def ensure_directory_exists(directory: Path) -> None:
    """Garante que o diretório existe, criando-o se necessário."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"{Colors.FAIL}Erro ao criar diretório {directory}: {e}{Colors.ENDC}")
        sys.exit(1)

def generate_tests(module_name: str) -> None:
    """Gera testes para um módulo específico."""
    # Cria o diretório de testes se não existir
    test_dir = TESTS_DIR / module_name
    ensure_directory_exists(test_dir)
    
    # Nome da classe baseado no nome do módulo (capitalizado, singular)
    class_name = module_name.capitalize()
    if class_name.endswith('s'):  # Torna singular se terminar com 's'
        class_name = class_name[:-1]
    
    # Gera o arquivo de testes
    test_file = test_dir / f"test_{module_name}.py"
    if not test_file.exists():
        test_file.write_text(get_test_content(module_name, class_name), encoding='utf-8')
        print(f"{Colors.OKGREEN}Criado: {test_file.relative_to(Path.cwd())}{Colors.ENDC}")
    
    # Gera o arquivo de configuração de testes
    conftest_file = test_dir / "conftest.py"
    if not conftest_file.exists():
        conftest_file.write_text(get_conftest_content(module_name, class_name), encoding='utf-8')
        print(f"{Colors.OKGREEN}Criado: {conftest_file.relative_to(Path.cwd())}{Colors.ENDC}")

def main():
    print(f"{Colors.HEADER}=== Gerador de Testes para Módulos ==={Colors.ENDC}/n")
    
    # Verifica se o diretório base existe
    if not BASE_DIR.exists():
        print(f"{Colors.FAIL}Erro: Diretório não encontrado: {BASE_DIR.absolute()}{Colors.ENDC}")
        print("Certifique-se de que o script está sendo executado a partir do diretório raiz do projeto.")
        sys.exit(1)
    
    # Lista os módulos disponíveis
    modules = [d.name for d in BASE_DIR.iterdir() 
              if d.is_dir() and d.name != "__pycache__" and (d / "endpoints.py").exists()]
    
    if not modules:
        print(f"{Colors.WARNING}Nenhum módulo com endpoints encontrado.{Colors.ENDC}")
        sys.exit(0)
    
    print(f"{Colors.OKBLUE}Módulos encontrados:{Colors.ENDC}")
    for i, module in enumerate(modules, 1):
        print(f"  {i}. {module}")
    
    # Pergunta ao usuário quais módulos atualizar
    print(f"/n{Colors.BOLD}Selecione os módulos para gerar testes (ex: 1,2,3 ou 'todos'):{Colors.ENDC}")
    while True:
        try:
            selection = input("> ").strip().lower()
            if selection == 'todos':
                selected_modules = modules
                break
            else:
                selected_indices = [int(i.strip()) - 1 for i in selection.split(',')]
                selected_modules = [modules[i] for i in selected_indices if 0 <= i < len(modules)]
                if selected_modules:
                    break
                print(f"{Colors.WARNING}Seleção inválida. Tente novamente.{Colors.ENDC}")
        except (ValueError, IndexError):
            print(f"{Colors.WARNING}Entrada inválida. Use números separados por vírgula ou 'todos'.{Colors.ENDC}")
        except (KeyboardInterrupt, EOFError):
            print("/nOperação cancelada pelo usuário.")
            sys.exit(0)
    
    # Gera os testes para os módulos selecionados
    print(f"/n{Colors.OKBLUE}Gerando testes...{Colors.ENDC}")
    for module in selected_modules:
        print(f"/n{Colors.BOLD}Módulo: {module}{Colors.ENDC}")
        generate_tests(module)
    
    print(f"/n{Colors.OKGREEN}✓ Processo concluído!{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"/n{Colors.FAIL}Erro inesperado: {e}{Colors.ENDC}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

