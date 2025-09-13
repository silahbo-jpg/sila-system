"""
Script de auditoria para encontrar referências ao módulo 'saude' no projeto.
"""
import os
import re
from pathlib import Path

def find_saude_references(sila_dev-system_dir):
    """Encontra referências a 'saude' nos arquivos do projeto."""
    sila_dev-system_path = Path(sila_dev-system_dir)
    pattern = re.compile(r'saude', re.IGNORECASE)
    
    print("🔍 Iniciando auditoria de referências a 'saude'...\n")
    
    # Extensões de arquivo para verificar
    extensions = ('.py', '.ts', '.js', '.json', '.md', '.yaml', '.yml', '.html')
    
    found = False
    
    for file_path in sila_dev-system_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if pattern.search(content):
                        print(f"⚠️  Referência encontrada em: {file_path.relative_to(sila_dev-system_path)}")
                        found = True
            except Exception as e:
                print(f"⚠️  Erro ao ler {file_path}: {e}")
    
    if not found:
        print("✅ Nenhuma referência a 'saude' encontrada no projeto.")
    else:
        print("\nℹ️  Foram encontradas referências a 'saude' nos arquivos acima.")
        print("   Por favor, atualize essas referências para 'health' antes de prosseguir.")

if __name__ == "__main__":
    project_sila_dev-system = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    find_saude_references(project_sila_dev-system)


