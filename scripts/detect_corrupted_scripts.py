import os
import py_compile

sila_dev-system_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
corrupted_files = []

print("🔍 Verificando scripts corrompidos...\n")

for dirpath, _, filenames in os.walk(sila_dev-system_DIR):
    for filename in filenames:
        if filename.endswith(".py"):
            filepath = os.path.join(dirpath, filename)
            try:
                py_compile.compile(filepath, doraise=True)
            except Exception as e:
                corrupted_files.append((filepath, str(e)))

if corrupted_files:
    print(f"🚨 {len(corrupted_files)} arquivos corrompidos encontrados:\n")
    for path, error in corrupted_files:
        print(f"❌ {path}\n   ↪️ {error}\n")
else:
    print("✅ Nenhum script corrompido encontrado.")

print("\n🔎 Verificação concluída.")


