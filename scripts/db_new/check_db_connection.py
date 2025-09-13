from dotenv import load_dotenv
import psycopg2
import os
from datetime import datetime

# 📋 Carregar variáveis do .env
load_dotenv()

# 🔍 Variáveis críticas
variaveis = [
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_HOST",
    "POSTGRES_PORT"
]

faltantes = [v for v in variaveis if not os.getenv(v)]
if faltantes:
    print(f"❌ Variáveis ausentes no .env: {', '.join(faltantes)}")
    exit(1)

# 🧠 Montar URL de conexão
db_url = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

# 🛠️ Testar conexão
try:
    conn = psycopg2.connect(**db_url)
    conn.close()
    print(f"✅ Conexão com banco PostgreSQL validada com sucesso — {db_url['host']}:{db_url['port']}/{db_url['dbname']}")
except Exception as e:
    print("❌ Falha na conexão com o banco:")
    print(f"   {type(e).__name__}: {e}")
    exit(1)
