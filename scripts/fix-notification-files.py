# scripts/fix-notification-files.py
"""
Corrige os 6 arquivos com nomes corrompidos relacionados a notificações.
Executa renomeação segura com feedback claro.
"""

import os
from pathlib import Path

# Diretório raiz do projeto
PROJECT_sila_dev-system = Path(__file__).parent.parent

# Lista de correções: (nome atual, nome correto)
CORRECTIONS = [
    ("backend/app/api/routes/nnnnnotifications.py", "backend/app/api/routes/notifications.py"),
    ("backend/app/core/nnnotificador.py", "backend/app/core/notificador.py"),
    ("backend/app/services/nnnnnnnotificacoes.py", "backend/app/services/notificacoes.py"),
    ("backend/app/services/nnnnnotifications.py", "backend/app/services/notifications.py"),
    ("backend/app/services/notification_service.py", "backend/app/services/notification_service.py"),  # Corrompido no nome do caminho
    ("backend/tests/test_nnnnnotifications.py", "backend/tests/test_notifications.py"),
]

def fix_file(current, correct):
    current_path = PROJECT_sila_dev-system / current
    correct_path = PROJECT_sila_dev-system / correct

    if current_path.exists():
        # Cria diretório pai se não existir
        correct_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            current_path.rename(correct_path)
            print(f"✅ {current} → {correct}")
        except Exception as e:
            print(f"❌ Erro ao renomear {current}: {e}")
    elif not correct_path.exists():
        print(f"❌ Arquivo não encontrado: {current} e {correct} não existe")
    else:
        print(f"🔍 Já corrigido: {correct}")

def main():
    print("🔧 Corrigindo arquivos com nomes corrompidos...")
    for current, correct in CORRECTIONS:
        fix_file(current, correct)
    print("✨ Correção de nomes concluída.")

if __name__ == "__main__":
    main()

