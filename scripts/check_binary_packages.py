import pkg_resources 
import os 
import sys

def has_native_binary(dist): 
    try: 
        for file in dist._get_metadata("RECORD"): 
            if file.endswith((".pyd", ".dll", ".so")): 
                return True 
    except Exception: 
        Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* 
    return False 

print("🔍 Pacotes com binários nativos:\n") 
for dist in pkg_resources.working_set: 
    if has_native_binary(dist): 
        print(f"⚠️ {dist.project_name} ({dist.version})") 

# Verificar sistema operacional
print(f"\n🎯 Sistema: {sys.platform}")
if sys.platform != "win32":
    print("❌ Aviso: Você não está no Windows!")
else:
    print("✅ Ambiente Windows confirmado")

