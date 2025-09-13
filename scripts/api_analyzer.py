#!/usr/bin/env python3
"""
API Endpoint Analyzer
Varre o diretório `backend` para encontrar e listar todos os endpoints da API,
organizando-os por método HTTP e salvando o resultado num arquivo Markdown.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

def find_endpoints_in_file(file_path: Path) -> List[Dict[str, str]]:
    """
    Procura por endpoints em um arquivo e extrai seu método e caminho.

    Args:
        file_path (Path): O caminho para o arquivo a ser analisado.

    Returns:
        List[Dict[str, str]]: Uma lista de dicionários, cada um contendo o
        método e o caminho de um endpoint encontrado.
    """
    endpoints = []
    # Expressão regular para encontrar decoradores de rotas do FastAPI
    # ex: @router.get("/users/")
    route_pattern = re.compile(r"@router\.(get|post|put|delete|patch|options)\([\"\'](.+?)[\"\']")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Encontra todas as correspondências no arquivo
            matches = route_pattern.finditer(content)
            for match in matches:
                method = match.group(1).upper()
                path = match.group(2)
                endpoints.append({"method": method, "path": path})
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo {file_path}: {e}")
    
    return endpoints

def main():
    """Função principal para analisar o diretório e gerar o relatório de endpoints."""
    # Define o diretório a ser analisado, que é o diretório `backend`
    # independentemente de onde o script é executado.
    base_dir = Path(__file__).parent.parent / "backend"
    
    if not base_dir.is_dir():
        print(f"Erro: O diretório '{base_dir}' não foi encontrado.")
        print("Certifique-se de que o script está na pasta `scripts` dentro do seu projeto.")
        return

    print(f"🔍 Analisando o diretório de backend: {base_dir}")
    
    found_endpoints = defaultdict(list)
    
    # Percorre o diretório `backend` e subdiretórios
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                
                # Ignora arquivos em diretórios que geralmente não contêm endpoints
                ignored_dirs = ['__pycache__', 'venv', '.venv', '.git', 'tests']
                if any(dir_name in str(file_path.parts) for dir_name in ignored_dirs):
                    continue

                # Extrai os endpoints do arquivo
                endpoints = find_endpoints_in_file(file_path)
                
                if endpoints:
                    relative_path = os.path.relpath(file_path, base_dir)
                    for ep in endpoints:
                        found_endpoints[ep['method']].append({
                            "path": ep['path'],
                            "file": str(relative_path)
                        })

    # Formata a saída em Markdown
    markdown_content = ["# Endpoints da API (Backend)",
                        "Este relatório lista todos os endpoints da API encontrados no projeto `backend`.",
                        "---", ""]

    methods_order = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    
    for method in methods_order:
        if found_endpoints[method]:
            markdown_content.append(f"### {method}")
            markdown_content.append("")
            for endpoint in sorted(found_endpoints[method], key=lambda x: x['path']):
                markdown_content.append(f"- `/{endpoint['path']}` (em: `{endpoint['file']}`)")
            markdown_content.append("")

    # Salva o arquivo Markdown na pasta `scripts`
    output_file = Path(__file__).parent / "api_endpoints.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(markdown_content))
        print(f"✅ Relatório de endpoints salvo em: {output_file}")
    except IOError as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

if __name__ == "__main__":
    main()
