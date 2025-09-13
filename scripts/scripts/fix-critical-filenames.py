# scripts/fix-critical-filenames.py
"""
Corrige nomes de arquivos críticos corrompidos no projeto sila_dev-system.
Foca nos arquivos com 'nnn' ou 'otif' no nome.
"""

import os
from pathlib import Path

PROJECT_sila_dev-system = Path(__file__).parent.parent
COUNTER = 0

# Mapeamento de correção (padrão corrompido → correto)
CORRECTIONS = {
    "nnn": "not",
    "otif": "notif",
    "otifier": "notifier",
    "otifications": "notifications",
    "otificacoes": "notificacoes",
}

def fix_filename(path: Path):
    global COUNTER
    original_name = path.name
    new_name = original_name

    for corrupt, correct in CORRECTIONS.items():
        new_name = new_name.replace(corrupt, correct)

    if new_name != original_name:
        new_path = path.parent / new_name
        try:
            path.rename(new_path)
            print(f"✅ {original_name} → {new_name}")
            COUNTER += 1
        except Exception as e:
            print(f"❌ Erro ao renomear {original_name}: {e}")

def main():
    print("🔍 Procurando arquivos com nomes corrompidos...")
    for file in PROJECT_sila_dev-system.rglob("*"):
        if file.is_file():
            for pattern in CORRECTIONS.keys():
                if pattern in file.name:
                    fix_filename(file)
                    break  # Evita múltiplas tentativas

    print(f"\n✨ {COUNTER} arquivos corrigidos com sucesso.")

if __name__ == "__main__":
    main()

