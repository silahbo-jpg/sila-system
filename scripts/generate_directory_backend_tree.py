#!/usr/bin/env python3
"""
Gerador de Árvore de Diretório Flexível
Gera uma representação visual em formato de árvore de um diretório especificado,
imprimindo-a no console e salvando-a num arquivo Markdown fixo.
"""

import os
import argparse
from pathlib import Path
from typing import List

# Diretórios e arquivos a serem ignorados na geração da árvore.
# Esta lista foi ajustada para permitir a exploração de subdiretórios importantes.
IGNORE_LIST: List[str] = [
    '.git',
    '.vscode',
    '__pycache__',
    '.venv',
    '.nodeenv',
    'venv',
    'test_venv',
    'node_modules',
    'dist',
    'build',
    # Arquivos fixos de documentação que não precisam ser duplicados.
    'project_tree.md',
    'directory_tree.md',
    # Arquivos de sistema e de configuração.
    '.gitignore',
    'docker-compose.yml',
    'config.yml',
    # Arquivos de log e relatórios.
    'alembic_upgrade_log.txt',
    'install-log.txt',
    'services_test_report.json',
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
        output.append(f"{prefix}└── [ERRO] Não é possível aceder a {directory.name}: {e}")
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
    """Função principal para gerar a árvore do diretório."""
    parser = argparse.ArgumentParser(description="Gera uma árvore visual do diretório especificado.")
    parser.add_argument("path", nargs='?', default=".", help="O caminho do diretório a ser analisado. Padrão: diretório atual.")
    args = parser.parse_args()

    # Define o diretório a ser analisado
    target_dir = Path(args.path).resolve()

    if not target_dir.is_dir():
        print(f"Erro: O caminho '{target_dir}' não é um diretório válido.")
        return

    print(f"🔍 Gerando árvore de arquivos para: {target_dir}")
    tree_lines = generate_tree(target_dir)
    tree_content = "\n".join(tree_lines)

    # O arquivo de saída agora é fixo para evitar confusão.
    output_filename = "project_tree.md"
    output_file = Path(__file__).parent / output_filename

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Árvore de Diretório para {target_dir.name}\n\n")
            f.write("Este documento fornece uma representação visual da estrutura de arquivos do diretório.\n\n")
            f.write("```\n")
            f.write(f"{target_dir.name}/\n{tree_content}\n")
            f.write("```\n")

        print("\n---")
        print(f"✅ Árvore do diretório salva em: {output_file}")
    except IOError as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

    # Imprime no console
    print("\n--- Árvore Gerada ---\n")
    print(f"{target_dir.name}/\n{tree_content}")
    print("\n---")

if __name__ == "__main__":
    main()
