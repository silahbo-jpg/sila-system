import os
import argparse
import csv
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
    log_md = [f"📄 Arquivo: `{caminho}`"]
    status_csv = {"arquivo": caminho}

    for chave, valor in VARIAVEIS_PADRAO.items():
        if chave not in existentes:
            linha = f"{chave}={valor}"
            novas_linhas.append(linha)
            log_md.append(f"➕ `{chave}` será adicionado")
            status_csv[chave] = "adicionado"
        else:
            log_md.append(f"✅ `{chave}` já presente")
            status_csv[chave] = "presente"

    if novas_linhas and not dry_run:
        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(novas_linhas) + "\n")

    return "\n".join(log_md), status_csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Simulação segura")
    args = parser.parse_args()

    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    envs = encontrar_envs(base)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"env_multi_preenchimento_{timestamp}.md"
    csv_path = f"env_multi_status_{timestamp}.csv"

    logs_md = [f"# 🧪 Preenchimento Multi-Arquivo (`--dry-run`={args.dry_run})", f"📅 {timestamp}", ""]
    registros_csv = []

    for env in envs:
        log_md, status_csv = preencher_env(env, dry_run=args.dry_run)
        logs_md.append(log_md)
        logs_md.append("---")
        registros_csv.append(status_csv)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(logs_md))

    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        campos = ["arquivo"] + list(VARIAVEIS_PADRAO.keys())
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros_csv)

    print(f"📋 Log Markdown salvo em: {log_path}")
    print(f"📊 Exportação CSV salva em: {csv_path}")

if __name__ == "__main__":
    main()
