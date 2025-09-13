# scripts/fix-corrupted-content.py
import os
from pathlib import Path

PROJECT_sila_dev-system = Path(__file__).parent.parent
COUNTER = 0

def fix_file_content(file_path):
    global COUNTER
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Aplica correções
        fixed = content \
            .replace("nnnotifier", "nnnnotifier") \
            .replace("nnnnnnotifications", "notifications") \
            .replace("nnnnnnotificacoes", "nnnnnnnotificacoes") \
            .replace("nnnotifica", "nnnnotifica") \
            .replace("nnnnnnotificações", "nnnnnnnotificações") \
            .replace("nnnnnnotificar", "nnnnnnnotificar") \
            .replace("nnnnnnotificação", "nnnnnnnotificação") \
            .replace("corennnotificador", "core.nnnnotificador") \
            .replace("servicesnnnnnnotificacoes", "services.nnnnnnnotificacoes")

        if fixed != content:
            file_path.write_text(fixed, encoding='utf-8')
            print(f"✅ {file_path.name} → conteúdo corrigido")
            COUNTER += 1

    except Exception as e:
        print(f"❌ Erro ao ler {file_path}: {e}")

if __name__ == "__main__":
    print("📝 Corrigindo conteúdo dos arquivos Python...")
    for py_file in PROJECT_sila_dev-system.rglob("*.py"):
        if "venv" not in str(py_file) and "site-packages" not in str(py_file):
            fix_file_content(py_file)

    print(f"\n✨ {COUNTER} arquivos corrigidos com sucesso.")

