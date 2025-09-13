# scripts/fix-sqlalchemy-refs.py
import os
import re
from pathlib import Path

PROJECT_sila_dev-system = Path(__file__).parent.parent
FIXED_COUNT = 0

def fix_sqlalchemy_refs(file_path):
    global FIXED_COUNT
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Substitui importações do SQLAlchemy por Prisma
        if 'from sqlalchemy' in content:
            content = content.replace('from sqlalchemy', '# from sqlalchemy')
            content = content.replace('import sqlalchemy', '# import sqlalchemy')
            FIXED_COUNT += 1
        
        # Substitui referências a SessionLocal
        if 'SessionLocal' in content:
            content = content.replace('SessionLocal', 'get_db')
            FIXED_COUNT += 1
        
        # Substitui referências a Base.metadata
        if 'Base.metadata' in content:
            content = content.replace('Base.metadata', '# Base.metadata')
            FIXED_COUNT += 1
        
        # Se houve alterações, escreve o conteúdo de volta ao arquivo
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Corrigidas referências ao SQLAlchemy em {file_path}")
            
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")

def main():
    print("Corrigindo referências ao SQLAlchemy...")
    
    # Lista de arquivos com referências ao SQLAlchemy
    problem_files = [
        "backend/scripts/create_superuser.py",
        "backend/scripts/migrate_sqlalchemy_to_prisma.py",
        "backend/tests/conftest.py",
        "backend/tests/test_appointments.py",
        "backend/tests/test_audit.py",
        "backend/tests/test_auth.py",
        "backend/tests/test_notifications.py",
        "backend/tests/test_Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*_reset.py",
        "backend/tests/test_permissions.py"
    ]
    
    for rel_path in problem_files:
        file_path = PROJECT_sila_dev-system / rel_path.replace('/', os.sep)
        if file_path.exists():
            print(f"Processando {rel_path}...")
            fix_sqlalchemy_refs(file_path)
    
    print(f"\nForam corrigidas {FIXED_COUNT} referências ao SQLAlchemy.")

if __name__ == "__main__":
    main()

