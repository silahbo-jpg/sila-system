import os
import sys
from dotenv import dotenv_values

RAIZ = os.getcwd()
VARIAVEIS_OBRIGATORIAS = ['DATABASE_URL', 'TEST_DATABASE_URL', 'READONLY_DATABASE_URL']
FALHAS = []

def validar_env(env_path):
    config = dotenv_values(env_path)
    for var in VARIAVEIS_OBRIGATORIAS:
        valor = config.get(var)
        if not valor:
            FALHAS.append(f"{env_path} está sem '{var}'")

def buscar_envs(raiz):
    for dirpath, _, filenames in os.walk(raiz):
        for nome in filenames:
            if nome.startswith('.env'):
                caminho_completo = os.path.join(dirpath, nome)
                validar_env(caminho_completo)

if __name__ == '__main__':
    buscar_envs(RAIZ)
    if FALHAS:
        print("\n❌ Falha na validação dos arquivos .env:")
        for falha in FALHAS:
            print(f" - {falha}")
        print("\n🚫 Commit bloqueado. Padronize os .env antes de prosseguir.\n")
        sys.exit(1)
    else:
        print("✅ Todos os arquivos .env estão padronizados.")
