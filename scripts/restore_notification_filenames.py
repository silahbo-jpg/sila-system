"""
Script para restaurar nomes corrompidos de arquivos de notificação.
Cria backups antes de fazer quaisquer alterações e processa apenas arquivos existentes.
"""
import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Diretórios
PROJECT_sila_dev-system = Path(__file__).parent.parent
BACKUP_DIR = PROJECT_sila_dev-system / "backups" / f"filename-fix-{datetime.now().strftime('%Y%m%d')}"

# Mapeamento de correções: (caminho_antigo, novo_nome)
CORRECTIONS = [
    ("backend/app/api/routes/nnnnnotifications.py", "notifications.py"),
    ("backend/app/core/nnnotificador.py", "notificador.py"),
    ("backend/app/services/nnnnnnnotificacoes.py", "notificacoes.py"),
    ("backend/app/services/nnnnnotifications.py", "notifications.py"),
    ("backend/app/services/notification_service.py", "notification_service.py"),
    ("backend/tests/test_nnnnnotifications.py", "test_notifications.py"),
]

def create_backup(file_path: Path):
    """Cria um backup do arquivo antes de qualquer modificação"""
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    backup_path = BACKUP_DIR / file_path.relative_to(PROJECT_sila_dev-system).with_name(
        f"{file_path.stem}_backup_{int(datetime.now().timestamp())}{file_path.suffix}"
    )
    
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, backup_path)
    return backup_path

def get_existing_files() -> List[Tuple[Path, Path]]:
    """Retorna lista de tuplas (caminho_antigo, novo_caminho) apenas para arquivos existentes"""
    existing_files = []
    for rel_old_path, new_filename in CORRECTIONS:
        old_path = PROJECT_sila_dev-system / rel_old_path
        if old_path.exists():
            new_path = old_path.parent / new_filename
            existing_files.append((old_path, new_path))
    return existing_files

def restore_filenames():
    print("🔍 Analisando arquivos para correção...")
    files_to_process = get_existing_files()
    
    if not files_to_process:
        print("✅ Nenhum arquivo para corrigir encontrado.")
        return
        
    print(f"🔧 Encontrados {len(files_to_process)} arquivo(s) para processar:")
    for old_path, new_path in files_to_process:
        print(f"   • {old_path.relative_to(PROJECT_sila_dev-system)} → {new_path.name}")
    
    print("\n⚠️  ATENÇÃO: Esta operação criará backups dos arquivos originais.")
    if input("   Deseja continuar? (s/n): ").lower() != 's':
        print("❌ Operação cancelada pelo usuário.")
        return
    
    success_count = 0
    
    for old_path, new_path in files_to_process:
        try:
            print(f"\n🔧 Processando: {old_path.relative_to(PROJECT_sila_dev-system)}")
            
            # Verifica se o arquivo de destino já existe
            if new_path.exists():
                if new_path.samefile(old_path):
                    print(f"   ✅ O arquivo já está com o nome correto: {new_path.name}")
                    success_count += 1
                    continue
                
                # Se o arquivo de destino existe e é diferente, faz backup
                backup_new_path = create_backup(new_path)
                print(f"   ⚠️  Arquivo de destino já existe. Backup criado em: {backup_new_path}")
            
            # Cria backup do arquivo original
            backup_path = create_backup(old_path)
            
            # Renomeia o arquivo
            old_path.rename(new_path)
            print(f"   ✅ Renomeado para: {new_path.name}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Erro ao processar: {str(e)}")
    
    print(f"\n✨ Concluído! {success_count}/{len(files_to_process)} arquivo(s) foram processados com sucesso.")
    print(f"📦 Backups disponíveis em: {BACKUP_DIR.relative_to(PROJECT_sila_dev-system) if BACKUP_DIR.is_relative_to(PROJECT_sila_dev-system) else BACKUP_DIR}")
    
    if success_count > 0:
        print("\n🔄 Reinicie o servidor para aplicar as alterações.")

if __name__ == "__main__":
    restore_filenames()


