#!/usr/bin/env python3
"""
SILA-System Project Tree Generator
Recursively generates a visual tree of the project's directory structure,
saving it to a Markdown file and printing it to the console.
"""

import os
from pathlib import Path
from typing import List

# Diretórios e arquivos a serem ignorados na geração da árvore.
IGNORE_LIST: List[str] = [
    '.git',
    '.vscode',
    '__pycache__',
    'venv',
    '.venv',
    'node_modules',
    'dist',
    'build',
    'binarios',
    'archived',
    'audit_reports',
    'scripts_index.md',
    'project_tree.md',
    'README.md',
    '.gitignore',
    'requirements.txt',
    'docker-compose.yml',
    'config.yml',
    # Adicione outros arquivos/diretórios que você queira ignorar.
]

def should_ignore(path: Path) -> bool:
    """Verifica se um dado caminho deve ser ignorado com base na lista de ignorados."""
    return any(p in path.parts for p in IGNORE_LIST) or path.name in IGNORE_LIST

def generate_tree(directory: Path, prefix: str = '', output: List[str] = None):
    """
    Gera recursivamente uma árvore de arquivos para o diretório dado.

    Args:
        directory (Path): O diretório inicial.
        prefix (str): O prefixo de indentação para a árvore.
        output (List[str]): A lista para adicionar as linhas da árvore.
    """
    if output is None:
        output = []

    try:
        # Ordena diretórios antes de arquivos para uma visualização mais limpa
        items = sorted(list(directory.iterdir()))
    except OSError as e:
        output.append(f"{prefix}└── [ERRO] Não é possível acessar {directory.name}: {e}")
        return output

    visible_items = [item for item in items if not should_ignore(item)]
    item_count = len(visible_items)
    
    for i, item in enumerate(visible_items):
        is_last = (i == item_count - 1)
        
        # Determina os caracteres corretos do ramo da árvore
        connector = '└── ' if is_last else '├── '
        new_prefix = prefix + ('    ' if is_last else '│   ')

        if item.is_dir():
            output.append(f"{prefix}{connector}{item.name}/")
            generate_tree(item, new_prefix, output)
        else:
            output.append(f"{prefix}{connector}{item.name}")

    return output

def main():
    """Função principal para gerar a árvore do projeto."""
    # Define a raiz do seu projeto
    root_dir = Path(__file__).parent.parent
    if not root_dir.exists():
        print(f"Erro: O diretório {root_dir} não existe.")
        return

    print(f"🔍 Gerando árvore de arquivos para: {root_dir}")
    tree_lines = generate_tree(root_dir)
    tree_content = "\n".join(tree_lines)

    # Salva em um arquivo Markdown
    output_file = Path(__file__).parent / 'project_tree.md'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Project Directory Tree\n\n")
            f.write("This document provides a visual representation of the project's file structure.\n\n")
            f.write("```\n")
            f.write(f"{root_dir.name}/\n{tree_content}\n")
            f.write("```\n")
        
        print("\n---")
        print(f"✅ Árvore do projeto salva em: {output_file}")
    except IOError as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

    # Imprime no console
    print("\n--- Árvore Gerada ---\n")
    print(f"{root_dir.name}/\n{tree_content}")
    print("\n---")

if __name__ == "__main__":
    main()
