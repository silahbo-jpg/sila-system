import sys
import os
import logging
import importlib
import psycopg2
from pathlib import Path

# Setup de logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "environment_check.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(msg, level="info"):
    print(msg)
    getattr(logging, level)(msg)

# 1. Versão do Python
log_and_print(f"✅ Python version: {sys.version}")

# 2. Teste de módulos
modules = [
    "os", "sys", "json", "logging", "requests", "fastapi", "sqlalchemy", "psycopg2", "pytest"
]
log_and_print("\\n🔍 Testando importação de módulos:")
for mod in modules:
    try:
        importlib.import_module(mod)
        log_and_print(f"✅ {mod} importado com sucesso")
    except ImportError:
        log_and_print(f"❌ Falha ao importar: {mod}", level="error")

# 3. Verificação de variáveis de ambiente
required_env_vars = ["DATABASE_URL", "API_KEY", "ENV"]
log_and_print("\\n🔍 Verificando variáveis de ambiente:")
for var in required_env_vars:
    if os.getenv(var):
        log_and_print(f"✅ {var} está definida")
    else:
        log_and_print(f"⚠️ {var} não está definida", level="warning")

# 4. Teste de conexão com sila_dev-systemQL
log_and_print("\\n🔍 Testando conexão com sila_dev-systemQL:")
db_url = os.getenv("DATABASE_URL")
if db_url:
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        log_and_print("✅ Conexão com sila_dev-systemQL bem-sucedida")
    except Exception as e:
        log_and_print(f"❌ Erro na conexão: {e}", level="error")
else:
    log_and_print("⚠️ DATABASE_URL não está definida", level="warning")

# 5. Verificação de estrutura de diretórios
log_and_print("\\n🔍 Verificando estrutura de diretórios:")
required_dirs = ["src", "tests", "scripts"]
for d in required_dirs:
    if Path(d).is_dir():
        log_and_print(f"✅ Diretório '{d}' existe")
    else:
        log_and_print(f"❌ Diretório '{d}' não encontrado", level="error")

log_and_print("\\n✅ Validação de ambiente concluída.")


