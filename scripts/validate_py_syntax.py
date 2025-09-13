#!/usr/bin/env python3
"""
Valida a sintaxe de todos os arquivos Python do projeto.
"""
import ast
import sys
from pathlib import Path

# Configuração
PROJECT_sila_dev-system = Path(__file__).parent.parent
IGNORE_DIRS = {
    '.git',
    '.venv',
    'venv',
    'env',
    '__pycache__',
    'node_modules',
    'site-packages',
    'migrations',
}

def validate_python_file(file_path: Path) -> list[tuple[Path, int, str]]:
    """Valida um único arquivo Python e retorna lista de erros."""
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        errors.append((file_path, e.lineno or 0, f"Erro de sintaxe: {e.msg}"))
    except UnicodeDecodeError:
        errors.append((file_path, 0, "Erro de decodificação: não é um arquivo de texto válido"))
    except Exception as e:
        errors.append((file_path, 0, f"Erro inesperado: {str(e)}"))
    return errors

def find_python_files() -> list[Path]:
    """Encontra todos os arquivos Python no projeto."""
    python_files = []
    for py_file in PROJECT_sila_dev-system.rglob('*.py'):
        # Pula diretórios ignorados
        if any(part in IGNORE_DIRS for part in py_file.parts):
            continue
        python_files.append(py_file)
    return python_files

def main():
    print("🔍 Validando sintaxe de arquivos Python...\n")
    
    python_files = find_python_files()
    total_files = len(python_files)
    print(f"Encontrados {total_files} arquivos Python para validar.")
    
    all_errors = []
    for i, py_file in enumerate(python_files, 1):
        rel_path = py_file.relative_to(PROJECT_sila_dev-system)
        print(f"  [{i}/{total_files}] Validando {rel_path}", end='\r')
        
        errors = validate_python_file(py_file)
        if errors:
            all_errors.extend(errors)
    
    # Resultados
    print("\n" + "="*80)
    if all_errors:
        print(f"❌ Foram encontrados {len(all_errors)} erros em {len({e[0] for e in all_errors})} arquivos:")
        for file_path, line, error in sorted(all_errors, key=lambda x: (str(x[0]), x[1])):
            rel_path = file_path.relative_to(PROJECT_sila_dev-system)
            print(f"\n{rel_path}:{line or '?'}")
            print(f"  {error}")
        sys.exit(1)
    else:
        print("✅ Todos os arquivos Python têm sintaxe válida!")
        sys.exit(0)

if __name__ == "__main__":
    main()


