"""
Script para atualizar as importações da classe Base nos modelos.

Este script substitui todas as ocorrências de 'from app.db.base_class import Base' por
'from app.db.base import Base' em todos os arquivos de modelo Python.
"""
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para permitir imports absolutos
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

# Diretórios a serem verificados
MODEL_DIRS = [
    PROJECT_ROOT / "app" / "models",
    PROJECT_ROOT / "app" / "modules"
]

# Padrão de busca
OLD_IMPORT = "from app.db.base_class import Base"
NEW_IMPORT = "from app.db.base import Base"

def update_file(file_path: Path) -> int:
    """Atualiza as importações em um único arquivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if OLD_IMPORT in content:
            new_content = content.replace(OLD_IMPORT, NEW_IMPORT)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Atualizado: {file_path}")
                return 1
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
    return 0

def main():
    """Procura e atualiza todos os arquivos de modelo."""
    updated_files = 0
    
    for models_dir in MODEL_DIRS:
        if not models_dir.exists():
            print(f"Aviso: Diretório não encontrado: {models_dir}")
            continue
            
        print(f"Procurando em: {models_dir}")
        
        # Encontra todos os arquivos Python nos diretórios de modelos
        for root, _, files in os.walk(models_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    file_path = Path(root) / file
                    updated_files += update_file(file_path)
    
    print(f"\nAtualização concluída. {updated_files} arquivos foram modificados.")

if __name__ == "__main__":
    main()
