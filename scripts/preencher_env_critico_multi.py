import os
import argparse
from datetime import datetime

VARIAVEIS_PADRAO = {
    "POSTGRES_USER": "devuser",
    "POSTGRES_PASSWORD": "Truman1_Marcelo1_1985",
    "POSTGRES_DB": "sila_db",
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": "5432",
    "DEBUG": "True",
    "SILA_SYSTEM_ID": "postgres-dev"
}

def encontrar_envs(caminho_base):
    envs = []
    for raiz, _, arquivos in os.walk(caminho_base):
        for nome in arquivos:
            if nome == ".env":
                envs.append(os.path.join(raiz, nome))
    return envs

def carregar_env(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    return {linha.split("=")[0]: linha.strip() for linha in linhas if "=" in linha}

def preencher_env(caminho, dry_run=False):
    existentes = carregar_env(caminho)
    novas_linhas = []
    log = [f"📄 Arquivo: `{caminho}`"]

    for chave, valor in VARIAVEIS_PADRAO.items():
        if chave not in existentes:
            linha = f"{chave}={valor}"
            novas_linhas.append(linha)
            log.append(f"➕ `{chave}` será adicionado")
        else:
            log.append(f"✅ `{chave}` já presente")

    if novas_linhas and not dry_run:
        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(novas_linhas) + "\n")

    return "\n".join(log)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Simulação segura")
    args = parser.parse_args()

    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    envs = encontrar_envs(base)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"env_multi_preenchimento_{timestamp}.md"

    logs = [f"# 🧪 Preenchimento Multi-Arquivo (`--dry-run`={args.dry_run})", f"📅 {timestamp}", ""]
    for env in envs:
        logs.append(preencher_env(env, dry_run=args.dry_run))
        logs.append("---")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))

    print(f"📋 Log consolidado salvo em: {log_path}")

if __name__ == "__main__":
    main()
