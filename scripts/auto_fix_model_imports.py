import os
import re
import shutil

# Diretório raiz e modelos
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "backend", "app", "db", "models")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "scripts", "model_backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

# Padrões a corrigir
FIXES = {
    "func.now()": {
        "usage": r"\bfunc\.now\(\)",
        "import": "from sqlalchemy import func"
    },
    "server_default=func.now()": {
        "usage": r"server_default\s*=\s*func\.now\(\)",
        "import": "from sqlalchemy import func"
    },
    "declarative_base()": {
        "usage": r"\bdeclarative_base\(\)",
        "import": "from sqlalchemy.orm import declarative_base"
    },
    "relationship()": {
        "usage": r"\brelationship\(",
        "import": "from sqlalchemy.orm import relationship"
    },
    "Base class usage": {
        "usage": r"class\s+\w+\(Base\)",
        "import": "from sqlalchemy.ext.declarative import declarative_base"
    }
}

def already_imported(content, import_line):
    return import_line in content or any(re.search(rf"{re.escape(import_line.split()[1])}", line) for line in content.splitlines() if "import" in line)

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fixed = False
    added_imports = []

    for label, pattern in FIXES.items():
        if re.search(pattern["usage"], content) and not already_imported(content, pattern["import"]):
            added_imports.append(pattern["import"])
            fixed = True

    if fixed:
        # Backup original
        shutil.copy(filepath, os.path.join(BACKUP_DIR, os.path.basename(filepath)))

        # Inserir imports após os primeiros imports existentes
        lines = content.splitlines()
        insert_index = next((i for i, line in enumerate(lines) if line.strip().startswith("import") or line.strip().startswith("from")), 0)
        for imp in added_imports:
            lines.insert(insert_index + 1, imp)
            insert_index += 1

        # Salvar arquivo corrigido
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return added_imports
    return []

def main():
    print(f"🔧 Corrigindo modelos em: {MODELS_DIR}")
    total_fixes = 0
    for root, _, files in os.walk(MODELS_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                added = fix_file(path)
                if added:
                    print(f"\n✅ Corrigido: {file}")
                    for imp in added:
                        print(f"   ➕ Import adicionado: {imp}")
                    total_fixes += len(added)
    if total_fixes == 0:
        print("\n✅ Nenhum ajuste necessário.")
    else:
        print(f"\n📋 Total de imports adicionados: {total_fixes}")
        print(f"🗂️ Backups salvos em: {BACKUP_DIR}")

if __name__ == "__main__":
    main()
