﻿# scripts/fix-syntax-errors.py
import os
import re
from pathlib import Path

PROJECT_sila_dev-system = Path(__file__).parent.parent
FIXED_COUNT = 0

def fix_syntax_errors(file_path):
    global FIXED_COUNT
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Remove BOM character (U+FEFF)
        if content.startswith('\ufeff'):
            content = content[1:]
            print(f"Removido BOM de {file_path}")
            FIXED_COUNT += 1
        
        # Corrige barras invertidas em f-strings
        if '\\' in content and 'f"' in content:
            # Substitui \n por \\n em f-strings
            pattern = r'f(["\'])(.+?)\\([nrtbfv\'"\\])(.+?)\1'
            fixed_content = re.sub(pattern, lambda m: f'f{m.group(1)}{m.group(2)}\\\\{m.group(3)}{m.group(4)}{m.group(1)}', content, flags=re.DOTALL)
            if fixed_content != content:
                content = fixed_content
                print(f"Corrigidas barras invertidas em f-strings em {file_path}")
                FIXED_COUNT += 1
        
        # Corrige caracteres após continuação de linha
        if '\\' in content:
            # Substitui \ seguido de espaço ou tab por apenas \
            pattern = r'\\[ \t]+'
            fixed_content = re.sub(pattern, r'\\\\\
', content)
            if fixed_content != content:
                content = fixed_content
                print(f"Corrigidos caracteres após continuação de linha em {file_path}")
                FIXED_COUNT += 1
        
        # Corrige sintaxe inválida comum
        # Substitui 'otif' por 'notif' em todo o conteúdo
        if 'otif' in content:
            fixed_content = content.replace('otif', 'notif')
            if fixed_content != content:
                content = fixed_content
                print(f"Corrigido 'otif' para 'notif' em {file_path}")
                FIXED_COUNT += 1
        
        # Escreve o conteúdo corrigido de volta ao arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")

def main():
    print("Corrigindo erros de sintaxe específicos...")
    
    # Lista de arquivos com erros conhecidos
    problem_files = [
        "backend/tests/modules/app/test_auth.py",
        "backend/tests/modules/app/test_citizen.py",
        "backend/tests/modules/app/test_protected.py",
        "backend/tests/modules/health/test_endpoints.py",
        "scripts/generate_tests.py",
        "scripts/quick_check.py",
        "scripts/setup_modules.py",
        "scripts/setup_project_structure.py",
        "scripts/setup_structure.py",
        "scripts/test_environment.py",

    ]
    
    for rel_path in problem_files:
        file_path = PROJECT_sila_dev-system / rel_path.replace('/', os.sep)
        if file_path.exists():
            print(f"Processando {rel_path}...")
            fix_syntax_errors(file_path)
    
    print(f"\nForam corrigidos {FIXED_COUNT} problemas de sintaxe.")

if __name__ == "__main__":
    main()

