#!/usr/bin/env python3
"""
Script para análise e documentação da migração de django-backend para backend FastAPI.

Este script gera um relatório detalhado comparando os diretórios e arquivos entre
o django-backend e o backend FastAPI, identificando possíveis conflitos e itens
que precisam de atenção durante a migração.
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Configurações
BASE_DIR = Path(__file__).parent.absolute()
DJANGO_BACKEND = BASE_DIR / 'django-backend'
FASTAPI_BACKEND = BASE_DIR / 'backend'
OUTPUT_FILE = BASE_DIR / 'migration_analysis_report.md'

class DirectoryAnalyzer:
    """Classe para análise de diretórios e geração de relatórios."""
    
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.files = {}
        self.dirs = {}
        
    def scan(self, path=None, prefix=''):
        """Varre recursivamente o diretório e coleta informações sobre arquivos e pastas."""
        if path is None:
            path = self.base_dir
            
        path = Path(path)
        
        for item in path.iterdir():
            relative_path = prefix + item.name
            
            if item.is_dir():
                # Ignora diretórios de ambiente virtual e cache
                if item.name in ('__pycache__', '.git', 'venv', 'env', '.venv', 'node_modules'):
                    continue
                    
                self.dirs[relative_path] = {
                    'path': str(item.relative_to(self.base_dir)),
                    'type': 'directory',
                    'size': self._get_dir_size(item)
                }
                # Recursão para subdiretórios
                self.scan(item, prefix=f"{relative_path}/")
                
            elif item.is_file():
                self.files[relative_path] = {
                    'path': str(item.relative_to(self.base_dir)),
                    'type': 'file',
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
    
    def _get_dir_size(self, path):
        """Calcula o tamanho total de um diretório em bytes."""
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Ignora links simbólicos
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)
        return total
    
    def get_summary(self):
        """Retorna um resumo da análise."""
        return {
            'directories': len(self.dirs),
            'files': len(self.files),
            'total_size': sum(f['size'] for f in self.files.values()) / (1024 * 1024),  # em MB
            'last_modified': max(
                [f['modified'] for f in self.files.values()], 
                default=datetime.now().isoformat()
            )
        }

def compare_directories(dir1, dir2):
    """Compara dois diretórios e retorna as diferenças."""
    analyzer1 = DirectoryAnalyzer(dir1)
    analyzer1.scan()
    
    analyzer2 = DirectoryAnalyzer(dir2)
    analyzer2.scan()
    
    # Encontra arquivos únicos em cada diretório
    unique_to_dir1 = set(analyzer1.files.keys()) - set(analyzer2.files.keys())
    unique_to_dir2 = set(analyzer2.files.keys()) - set(analyzer1.files.keys())
    
    # Encontra arquivos comuns mas com tamanhos diferentes
    common_files = set(analyzer1.files.keys()) & set(analyzer2.files.keys())
    different_sizes = [
        f for f in common_files 
        if analyzer1.files[f]['size'] != analyzer2.files[f]['size']
    ]
    
    return {
        'dir1_summary': analyzer1.get_summary(),
        'dir2_summary': analyzer2.get_summary(),
        'unique_to_dir1': sorted(list(unique_to_dir1)),
        'unique_to_dir2': sorted(list(unique_to_dir2)),
        'different_sizes': different_sizes,
        'scan_time': datetime.now().isoformat()
    }

def generate_markdown_report(comparison, dir1_name, dir2_name):
    """Gera um relatório em Markdown com os resultados da comparação."""
    report = [
        "# Análise de Migração: Django para FastAPI/n",
        f"**Data da análise:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}/n",
        "## Resumo da Análise/n",
        f"### {dir1_name} (Django)/n",
        f"- Diretórios: {comparison['dir1_summary']['directories']}",
        f"- Arquivos: {comparison['dir1_summary']['files']}",
        f"- Tamanho total: {comparison['dir1_summary']['total_size']:.2f} MB/n",
        
        f"### {dir2_name} (FastAPI)/n",
        f"- Diretórios: {comparison['dir2_summary']['directories']}",
        f"- Arquivos: {comparison['dir2_summary']['files']}",
        f"- Tamanho total: {comparison['dir2_summary']['total_size']:.2f} MB/n",
        
        "## Itens que Requerem Atenção/n",
        f"### Arquivos Exclusivos em {dir1_name} (Django)/n"
    ]
    
    # Lista arquivos exclusivos do Django
    if comparison['unique_to_dir1']:
        for file in comparison['unique_to_dir1']:
            report.append(f"- `{file}`")
    else:
        report.append("Nenhum arquivo exclusivo encontrado./n")
    
    report.append(f"/n### Arquivos com Tamanhos Diferentes/n")
    
    # Lista arquivos com tamanhos diferentes
    if comparison['different_sizes']:
        for file in comparison['different_sizes']:
            report.append(f"- `{file}`")
    else:
        report.append("Nenhum arquivo com tamanho diferente encontrado./n")
    
    # Recomendações
    report.extend([
        "/n## Recomendações para Migração/n",
        "1. **Backup completo** antes de qualquer alteração",
        "2. **Migrar dados** do banco SQLite do Django para o banco do FastAPI",
        "3. **Verificar dependências** do requirements.txt",
        "4. **Testar exaustivamente** após a migração",
        "5. **Manter o diretório django-backend** por algum tempo após a migração/n",
        "## Próximos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*os/n",
        "1. Revisar os arquivos listados acima",
        "2. Criar plano de migração para cada funcionalidade",
        "3. Implementar migração em ambiente de teste",
        "4. Validar funcionamento",
        "5. Planejar deploy em produção"
    ])
    
    return '/n'.join(report)

def main():
    """Função principal."""
    print(f"Analisando diretórios...")
    print(f"- Django: {DJANGO_BACKEND}")
    print(f"- FastAPI: {FASTAPI_BACKEND}")
    
    # Verifica se os diretórios existem
    if not DJANGO_BACKEND.exists() or not FASTAPI_BACKEND.exists():
        print("Erro: Um ou ambos os diretórios não existem.")
        return
    
    # Realiza a análise comparativa
    print("/nComparando diretórios...")
    comparison = compare_directories(DJANGO_BACKEND, FASTAPI_BACKEND)
    
    # Gera o relatório
    print("Gerando relatório...")
    report = generate_markdown_report(
        comparison, 
        dir1_name="django-backend",
        dir2_name="backend"
    )
    
    # Salva o relatório
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"/n✅ Análise concluída! Relatório salvo em: {OUTPUT_FILE}")
    print("/nPróximos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*os:")
    print(f"1. Revise o relatório em {OUTPUT_FILE}")
    print("2. Crie um backup do diretório django-backend")
    print("3. Documente o plano de migração")
    print("4. Execute a migração em ambiente de teste")

if __name__ == "__main__":
    main()


