import os
import re

def update_model_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Verificar se o arquivo já importa Base de app.core.db.db
    if "from app.core.db.db import Base" in content:
        print(f"Arquivo {file_path} já importa Base corretamente.")
        return False
    
    # Substituir importação de declarative_base
    content = re.sub(
        r'from sqlalchemy\.ext\.declarative import declarative_base',
        'from app.core.db.db import Base',
        content
    )
    
    # Remover definição de Base = declarative_base()
    content = re.sub(r'\nBase = declarative_base\(\)\n', '\n', content)
    
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Atualizado: {file_path}")
    return True

def find_and_update_models():
    models_dir = 'backend/app/models'
    updated_files = 0
    
    for root, _, files in os.walk(models_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'declarative_base()' in content:
                        if update_model_file(file_path):
                            updated_files += 1
    
    return updated_files

if __name__ == "__main__":
    print("Atualizando modelos para usar Base de app.core.db.db...")
    updated = find_and_update_models()
    print(f"Total de {updated} arquivos atualizados.")

