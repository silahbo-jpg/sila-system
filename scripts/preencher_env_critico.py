import sys
from pathlib import Path
from datetime import datetime
from dotenv import dotenv_values

# 📌 Variáveis críticas e seus valores padrão
VARIAVEIS_CRITICAS = {
    "POSTGRES_USER": "devuser",
    "POSTGRES_PASSWORD": "Truman1_Marcelo1_1985",
    "POSTGRES_DB": "sila_db",
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": "5432",
    "DEBUG": "True",
    "SILA_SYSTEM_ID": "postgres-dev"
}

DRY_RUN = "--dry-run" in sys.argv
env_path = Path(".env")
log_path = Path(f"env_preenchimento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

# 🔍 Carregar conteúdo atual
config = dotenv_values(env_path)
linhas = env_path.read_text(encoding="utf-8").splitlines()

# 📋 Log institucional
log = [f"# 🧪 Preenchimento automático do .env\n",
       f"**Arquivo auditado:** `{env_path.resolve()}`\n",
       f"**Modo:** `{'Simulação segura' if DRY_RUN else 'Execução real'}`\n",
       "## Variáveis processadas:\n"]

# 🔁 Preencher variáveis ausentes
for chave, valor_padrao in VARIAVEIS_CRITICAS.items():
    if chave not in config or config[chave].strip() == "":
        log.append(f"- ⚠️ `{chave}` ausente → será preenchido com `{valor_padrao}`")
        if not DRY_RUN:
            linhas.append(f'{chave}="{valor_padrao}"')
    else:
        log.append(f"- ✅ `{chave}` já presente: `{config[chave]}`")

# 💾 Escrever alterações (se não for dry-run)
if not DRY_RUN:
    env_path.write_text("\n".join(linhas), encoding="utf-8")

# 📝 Salvar log
log_path.write_text("\n".join(log), encoding="utf-8")
print(f"📋 Preenchimento concluído. Log salvo em: {log_path}")
