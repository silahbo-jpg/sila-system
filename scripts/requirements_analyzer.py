#!/usr/bin/env python3
"""
Analisador de Dependências do Projeto
Varre o diretório `backend` para encontrar e analisar todos os arquivos
de requisitos, identificando pacotes, versões e duplicações.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

def find_requirements_files(directory: Path) -> List[Path]:
    """
    Procura por todos os arquivos de requisitos no diretório dado.
    
    Args:
        directory (Path): O diretório base para a pesquisa.
        
    Returns:
        List[Path]: Uma lista de caminhos para os arquivos encontrados.
    """
    # Procura por arquivos que comecem com "requirements" e terminem com ".txt"
    return list(directory.rglob('requirements*.txt'))

def parse_requirements_file(file_path: Path) -> Set[Tuple[str, str]]:
    """
    Lê e analisa um arquivo de requisitos, extraindo pacotes e versões.
    
    Args:
        file_path (Path): O caminho para o arquivo a ser analisado.
        
    Returns:
        Set[Tuple[str, str]]: Um conjunto de tuplos (nome_pacote, versao).
    """
    packages = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(('#', '-e', '-r')):
                    continue
                
                # Usa regex para extrair o nome do pacote e a versão
                match = re.match(r'^([a-zA-Z0-9_-]+)(?:==([0-9.]+))?.*$', line)
                if match:
                    package_name = match.group(1)
                    version = match.group(2) if match.group(2) else "any"
                    packages.add((package_name, version))
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo {file_path}: {e}")
        
    return packages

def main():
    """Função principal para encontrar e analisar as dependências."""
    # Define o diretório a ser analisado
    base_dir = Path(__file__).parent.parent / "backend"
    
    if not base_dir.is_dir():
        print(f"Erro: O diretório '{base_dir}' não foi encontrado.")
        return
        
    print(f"🔍 Analisando dependências no diretório: {base_dir}")
    
    req_files = find_requirements_files(base_dir)
    if not req_files:
        print("Nenhum arquivo 'requirements*.txt' encontrado. Análise cancelada.")
        return
    
    all_packages: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
    
    for file_path in req_files:
        packages = parse_requirements_file(file_path)
        for name, version in packages:
            all_packages[name][version].append(file_path.name)
            
    # Formata a saída em Markdown
    markdown_content = ["# Relatório de Dependências",
                        "Este relatório lista todos os pacotes encontrados nos arquivos de requisitos, ",
                        "identificando versões e ocorrências.\n",
                        "---", ""]

    sorted_packages = sorted(all_packages.keys())
    
    # Adiciona a lista de pacotes
    markdown_content.append("## Pacotes Encontrados")
    markdown_content.append("```")
    for package_name in sorted_packages:
        versions = all_packages[package_name]
        version_strings = [f"{v} ({', '.join(files)})" for v, files in versions.items()]
        markdown_content.append(f"{package_name}: {', '.join(version_strings)}")
    markdown_content.append("```\n")

    # Identifica e reporta duplicados e inconsistências
    markdown_content.append("## Análise de Duplicação e Inconsistência")
    markdown_content.append("")
    
    duplicate_found = False
    for package_name in sorted_packages:
        versions = all_packages[package_name]
        if len(versions) > 1:
            duplicate_found = True
            markdown_content.append(f"### ⚠️ {package_name} - Múltiplas Versões Encontradas!")
            markdown_content.append("")
            for version, files in versions.items():
                markdown_content.append(f"- Versão `{version}` encontrada em: {', '.join(files)}")
            markdown_content.append("")
    
    if not duplicate_found:
        markdown_content.append("✅ Nenhuma duplicação de pacotes ou inconsistência de versão encontrada.")

    # Salva o arquivo Markdown na pasta `scripts`
    output_file = Path(__file__).parent / "dependency_report.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(markdown_content))
        print(f"✅ Relatório de dependências salvo em: {output_file}")
    except IOError as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

if __name__ == "__main__":
    main()
