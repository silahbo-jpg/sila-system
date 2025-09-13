#!/bin/bash

# Script de migração e padronização do projeto SILA
# Este script deve ser executado no terminal WSL (Ubuntu)

set -e  # Interrompe o script se algum comando falhar

echo "===== Iniciando processo de padronização e migração para PostgreSQL ====="
echo ""

# Diretório base do projeto
BASE_DIR="$HOME/SGI/sila/sila-system"
cd "$BASE_DIR"

echo "===== 1. Padronizando nomenclatura e estrutura ====="

# 1.1 Verificar e padronizar requirements_test.txt
if [ -f "backend/requirements-test.txt" ] && [ ! -f "backend/requirements_test.txt" ]; then
    echo "Renomeando requirements-test.txt para requirements_test.txt..."
    mv backend/requirements-test.txt backend/requirements_test.txt
elif [ -f "backend/requirements-test.txt" ] && [ -f "backend/requirements_test.txt" ]; then
    echo "Ambos os arquivos requirements-test.txt e requirements_test.txt existem."
    echo "Verificando diferenças..."
    diff -u backend/requirements-test.txt backend/requirements_test.txt || true
    echo "Mantendo requirements_test.txt e removendo requirements-test.txt..."
    rm backend/requirements-test.txt
fi

# 1.2 Verificar e padronizar pytest.ini
if [ -f "backend/pytest.inies" ] && [ -f "backend/pytest.ini" ]; then
    echo "Ambos os arquivos pytest.ini e pytest.inies existem."
    echo "Verificando diferenças..."
    diff -u backend/pytest.ini backend/pytest.inies || true
    echo "Mantendo pytest.ini e removendo pytest.inies..."
    rm backend/pytest.inies
elif [ -f "backend/pytest.inies" ] && [ ! -f "backend/pytest.ini" ]; then
    echo "Renomeando pytest.inies para pytest.ini..."
    mv backend/pytest.inies backend/pytest.ini
fi

# 1.3 Atualizar requirements_test.txt para incluir pytest-cov
if [ -f "backend/requirements_test.txt" ]; then
    echo "Atualizando requirements_test.txt para incluir pytest-cov..."
    if ! grep -q "pytest-cov" backend/requirements_test.txt; then
        echo "pytest-cov==4.1.0" >> backend/requirements_test.txt
        echo "Adicionado pytest-cov==4.1.0 ao requirements_test.txt"
    else
        echo "pytest-cov já está incluído em requirements_test.txt"
    fi
fi

echo ""
echo "===== 2. Configurando conexão com PostgreSQL ====="

# 2.1 Criar diretório db se não existir
mkdir -p backend/app/core/db

# 2.2 Criar arquivo db.py
echo "Criando arquivo db.py..."
cat > backend/app/core/db/db.py << 'EOF'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sila.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
EOF

# 2.3 Criar arquivo __init__.py no diretório db
touch backend/app/core/db/__init__.py

# 2.4 Criar/atualizar arquivo .env
echo "Criando/atualizando arquivo .env..."
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env 2>/dev/null || touch backend/.env
fi

echo "Configurando DATABASE_URL no .env..."
if grep -q "DATABASE_URL" backend/.env; then
    # Substituir a linha existente
    sed -i 's|^DATABASE_URL=.*$|DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sila_dev|g' backend/.env
else
    # Adicionar nova linha
    echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sila_dev" >> backend/.env
fi

# 2.5 Atualizar requirements.txt para incluir psycopg2-binary
echo "Atualizando requirements.txt para incluir psycopg2-binary..."
if ! grep -q "psycopg2-binary" backend/requirements.txt; then
    echo "psycopg2-binary==2.9.5" >> backend/requirements.txt
    echo "Adicionado psycopg2-binary==2.9.5 ao requirements.txt"
else
    echo "psycopg2-binary já está incluído em requirements.txt"
fi

# 2.6 Verificar se alembic está instalado
if ! grep -q "alembic" backend/requirements.txt; then
    echo "alembic==1.8.1" >> backend/requirements.txt
    echo "Adicionado alembic==1.8.1 ao requirements.txt"
else
    echo "alembic já está incluído em requirements.txt"
fi

echo ""
echo "===== 3. Buscando modelos que precisam ser atualizados ====="

# 3.1 Encontrar arquivos que usam declarative_base()
echo "Procurando por arquivos que usam declarative_base()..."
GREP_RESULT=$(grep -r "declarative_base()" backend/app/models/ 2>/dev/null || echo "Nenhum arquivo encontrado")
echo "$GREP_RESULT"

# 3.2 Criar script para atualizar modelos
echo "Criando script para atualizar modelos..."
cat > update_models.py << 'EOF'
import os
import re

def update_model_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Verificar se o arquivo já importa Base de app.core.db.db
    if "from app.core.db.db import Base" in content:
        print(f"Arquivo {file_path} já importa Base corretamente.")
        return False
    
    # Substituir importação de declarative_base
    content = re.sub(
        r'from sqlalchemy\.ext\.declarative import declarative_base',
        'from app.core.db.db import Base',
        content
    )
    
    # Remover definição de Base = declarative_base()
    content = re.sub(r'\nBase = declarative_base\(\)\n', '\n', content)
    
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Atualizado: {file_path}")
    return True

def find_and_update_models():
    models_dir = 'backend/app/models'
    updated_files = 0
    
    for root, _, files in os.walk(models_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'declarative_base()' in content:
                        if update_model_file(file_path):
                            updated_files += 1
    
    return updated_files

if __name__ == "__main__":
    print("Atualizando modelos para usar Base de app.core.db.db...")
    updated = find_and_update_models()
    print(f"Total de {updated} arquivos atualizados.")
EOF

# Executar script para atualizar modelos
python update_models.py

echo ""
echo "===== 4. Configurando testes com cobertura ====="

# 4.1 Atualizar .coveragerc
echo "Atualizando .coveragerc..."
cat > backend/.coveragerc << 'EOF'
[run]
source = app
omit = 
    app/tests/*
    app/*/__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError
EOF

# 4.2 Criar script para executar testes com cobertura
echo "Criando script para executar testes com cobertura..."
mkdir -p backend/scripts
cat > backend/scripts/run_tests_with_coverage.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"/.. || exit

# Executar testes com cobertura
python -m pytest --cov=app --cov-report=term --cov-report=html:coverage_html

# Exibir resumo da cobertura
echo "\nResumo da cobertura de testes:\n"
cat .coverage | grep -v "pragma: no cover" | wc -l

# Abrir relatório HTML se disponível
if command -v xdg-open > /dev/null; then
  xdg-open coverage_html/index.html &
fi
EOF

# Tornar o script executável
chmod +x backend/scripts/run_tests_with_coverage.sh

echo ""
echo "===== 5. Criando script de migração de SQLite para PostgreSQL ====="

# 5.1 Criar script de migração
mkdir -p scripts
cat > scripts/migrate_sqlite_to_postgres.py << 'EOF'
import os
import sys
import sqlite3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv("backend/.env")

# Configurações
SQLITE_DB_PATH = "backend/sila.db"
PG_CONNECTION = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/sila_dev")

# Extrair componentes da string de conexão PostgreSQL
db_parts = PG_CONNECTION.replace("postgresql://", "").split("/")
db_name = db_parts[1] if len(db_parts) > 1 else "sila_dev"
db_conn = db_parts[0].split("@")
db_user_pass = db_conn[0].split(":")
db_user = db_user_pass[0]
db_pass = db_user_pass[1] if len(db_user_pass) > 1 else ""
db_host_port = db_conn[1].split(":")
db_host = db_host_port[0]
db_port = db_host_port[1] if len(db_host_port) > 1 else "5432"

def create_postgres_db():
    """Cria o banco de dados PostgreSQL se não existir"""
    try:
        # Conectar ao PostgreSQL sem especificar um banco de dados
        conn = psycopg2.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar se o banco de dados já existe
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Criando banco de dados '{db_name}'...")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Banco de dados '{db_name}' criado com sucesso!")
        else:
            print(f"Banco de dados '{db_name}' já existe.")
            
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao criar banco de dados PostgreSQL: {e}")
        return False

def get_sqlite_tables():
    """Obtém a lista de tabelas do SQLite"""
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        print(f"Erro ao obter tabelas do SQLite: {e}")
        return []

def get_table_schema(table_name):
    """Obtém o esquema de uma tabela SQLite"""
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema = []
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, is_pk = col
            # Mapear tipos SQLite para PostgreSQL
            pg_type = map_sqlite_to_pg_type(col_type)
            constraints = []
            
            if is_pk:
                constraints.append("PRIMARY KEY")
            if not_null:
                constraints.append("NOT NULL")
            if default_val is not None:
                if default_val.isdigit() or default_val in ['true', 'false']:
                    constraints.append(f"DEFAULT {default_val}")
                else:
                    constraints.append(f"DEFAULT '{default_val}'")
                    
            schema.append({
                "name": col_name,
                "type": pg_type,
                "constraints": " ".join(constraints)
            })
            
        cursor.close()
        conn.close()
        return schema
    except Exception as e:
        print(f"Erro ao obter esquema da tabela {table_name}: {e}")
        return []

def map_sqlite_to_pg_type(sqlite_type):
    """Mapeia tipos SQLite para tipos PostgreSQL"""
    sqlite_type = sqlite_type.upper()
    if "INT" in sqlite_type:
        return "INTEGER"
    elif "CHAR" in sqlite_type or "TEXT" in sqlite_type or "CLOB" in sqlite_type:
        return "TEXT"
    elif "REAL" in sqlite_type or "FLOA" in sqlite_type or "DOUB" in sqlite_type:
        return "FLOAT"
    elif "BOOL" in sqlite_type:
        return "BOOLEAN"
    elif "BLOB" in sqlite_type:
        return "BYTEA"
    elif "DATE" in sqlite_type:
        return "DATE"
    elif "TIME" in sqlite_type:
        if "TIMESTAMP" in sqlite_type:
            return "TIMESTAMP"
        return "TIME"
    else:
        return "TEXT"  # Tipo padrão

def create_pg_table(table_name, schema):
    """Cria uma tabela no PostgreSQL"""
    try:
        conn = psycopg2.connect(PG_CONNECTION)
        cursor = conn.cursor()
        
        # Construir a declaração CREATE TABLE
        columns = [f"\"{col['name']}\" {col['type']} {col['constraints']}" for col in schema]
        create_stmt = f"CREATE TABLE IF NOT EXISTS \"{table_name}\" ({', '.join(columns)});"
        
        print(f"Criando tabela {table_name}...")
        cursor.execute(create_stmt)
        conn.commit()
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao criar tabela {table_name} no PostgreSQL: {e}")
        return False

def migrate_table_data(table_name):
    """Migra dados de uma tabela SQLite para PostgreSQL"""
    try:
        # Conectar ao SQLite
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obter dados da tabela SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"Tabela {table_name} está vazia. Nada para migrar.")
            sqlite_cursor.close()
            sqlite_conn.close()
            return True
        
        # Obter nomes das colunas
        sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in sqlite_cursor.fetchall()]
        
        # Conectar ao PostgreSQL
        pg_conn = psycopg2.connect(PG_CONNECTION)
        pg_cursor = pg_conn.cursor()
        
        # Limpar tabela PostgreSQL antes de inserir
        pg_cursor.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;')
        
        # Preparar declaração INSERT
        placeholders = ", ".join(["%s"] * len(columns))
        insert_stmt = f'INSERT INTO "{table_name}" ("{\"\, \"".join(columns)}") VALUES ({placeholders})'
        
        # Inserir dados em lotes
        batch_size = 100
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            pg_cursor.executemany(insert_stmt, batch)
            pg_conn.commit()
            print(f"Migrados {min(i+batch_size, len(rows))}/{len(rows)} registros para {table_name}")
        
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
        print(f"Migração de dados para {table_name} concluída com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao migrar dados da tabela {table_name}: {e}")
        return False

def main():
    print("===== Iniciando migração de SQLite para PostgreSQL =====")
    
    # Verificar se o arquivo SQLite existe
    if not os.path.exists(SQLITE_DB_PATH):
        print(f"Erro: Banco de dados SQLite não encontrado em {SQLITE_DB_PATH}")
        return False
    
    # Criar banco de dados PostgreSQL
    if not create_postgres_db():
        return False
    
    # Obter tabelas do SQLite
    tables = get_sqlite_tables()
    if not tables:
        print("Nenhuma tabela encontrada no banco de dados SQLite.")
        return False
    
    print(f"Encontradas {len(tables)} tabelas: {', '.join(tables)}")
    
    # Migrar cada tabela
    for table in tables:
        print(f"\nProcessando tabela: {table}")
        schema = get_table_schema(table)
        if not schema:
            print(f"Erro ao obter esquema da tabela {table}. Pulando...")
            continue
        
        if create_pg_table(table, schema):
            migrate_table_data(table)
    
    print("\n===== Migração concluída! =====")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

echo ""
echo "===== Processo de configuração concluído com sucesso! ====="
echo ""
echo "Para completar a migração, execute os seguintes comandos:"
echo ""
echo "1. Instalar dependências:"
echo "   cd $BASE_DIR/backend && pip install -r requirements.txt"
echo ""
echo "2. Migrar dados do SQLite para PostgreSQL:"
echo "   cd $BASE_DIR && python scripts/migrate_sqlite_to_postgres.py"
echo ""
echo "3. Executar testes com cobertura:"
echo "   cd $BASE_DIR/backend && ./scripts/run_tests_with_coverage.sh"
echo ""
echo "===== Fim do script ====="
