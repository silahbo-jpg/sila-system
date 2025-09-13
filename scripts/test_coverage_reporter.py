#!/usr/bin/env python3
"""
Gerador de Relatório de Cobertura de Testes
Executa os testes do projeto e gera um relatório de cobertura em Markdown.
"""

import subprocess
import json
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

def run_tests_and_get_coverage(backend_dir: Path) -> dict:
    """
    Executa os testes pytest com cobertura e retorna os dados de cobertura.
    
    Args:
        backend_dir (Path): O caminho para o diretório 'backend'.
        
    Returns:
        dict: O dicionário de dados de cobertura.
    """
    # Executa pytest com as opções de cobertura e formato de saída JSON
    print("🚀 A executar testes com cobertura...")
    command = [
        "pytest",
        str(backend_dir / "tests"),
        f"--rootdir={backend_dir}",
        f"--cov={backend_dir}/app",
        "--cov-report=json"
    ]
    
    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Lê o relatório de cobertura gerado
        coverage_file = Path(".coverage.json")
        if not coverage_file.exists():
            print("❌ O arquivo de relatório de cobertura (.coverage.json) não foi encontrado.")
            return {}
            
        with open(coverage_file, 'r', encoding='utf-8') as f:
            coverage_data = json.load(f)
            
        os.remove(coverage_file)
        return coverage_data

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar os testes: {e.stderr}")
        print("Certifique-se de que o pytest e o pytest-cov estão instalados.")
        print("Pode instalá-los com: pip install pytest pytest-cov")
        return {}

def generate_markdown_report(coverage_data: dict) -> str:
    """
    Gera o conteúdo do relatório de cobertura em formato Markdown.
    
    Args:
        coverage_data (dict): Os dados de cobertura do JSON.
        
    Returns:
        str: O conteúdo do relatório em Markdown.
    """
    if not coverage_data:
        return "Nenhum dado de cobertura disponível. Por favor, corrija os erros de execução."

    markdown_content = ["# Relatório de Cobertura de Testes\n",
                        "Este relatório fornece uma visão geral da cobertura de testes do projeto `backend`.\n",
                        "---\n"]

    summary = coverage_data.get('totals', {})
    
    # Resumo Geral
    markdown_content.append("## Resumo Geral\n")
    markdown_content.append(f"- **Linhas Cobertas:** `{summary.get('covered_lines', 0)}`")
    markdown_content.append(f"- **Linhas Não Cobertas:** `{summary.get('missing_lines', 0)}`")
    markdown_content.append(f"- **Linhas Executáveis:** `{summary.get('num_statements', 0)}`")
    markdown_content.append(f"- **Cobertura Total:** `{summary.get('percent_covered', 0):.2f}%`\n")
    
    # Detalhes por Arquivo
    markdown_content.append("## Cobertura por Arquivo\n")
    markdown_content.append("| Arquivo | Cobertura | Linhas Não Cobertas |")
    markdown_content.append("|---|---|---|")
    
    files_data = coverage_data.get('files', {})
    sorted_files = sorted(files_data.keys())
    
    for file_path in sorted_files:
        file_summary = files_data[file_path].get('summary', {})
        percent = file_summary.get('percent_covered', 0)
        missing_lines = file_summary.get('missing_lines', [])
        missing_lines_str = ', '.join(map(str, missing_lines)) if missing_lines else "N/A"
        
        markdown_content.append(
            f"| `{file_path}` | `{percent:.2f}%` | `{missing_lines_str}` |"
        )
    
    return "\n".join(markdown_content)

def main():
    """Função principal para executar e salvar o relatório."""
    print("🔍 A iniciar análise de cobertura de testes...")
    
    backend_dir = Path(__file__).parent.parent / "backend"
    scripts_dir = Path(__file__).parent
    
    if not backend_dir.is_dir():
        print(f"Erro: O diretório '{backend_dir}' não foi encontrado.")
        return
        
    coverage_data = run_tests_and_get_coverage(backend_dir)
    
    markdown_report = generate_markdown_report(coverage_data)
    
    output_file = scripts_dir / "coverage_report.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        print(f"✅ Relatório de cobertura salvo em: {output_file}")
    except IOError as e:
        print(f"❌ Erro ao salvar o relatório: {e}")

if __name__ == "__main__":
    main()
