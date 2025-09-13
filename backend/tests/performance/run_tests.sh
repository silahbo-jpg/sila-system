#!/bin/bash

# Script para executar testes de performance do módulo Citizenship

# Configurações
LOCUSTFILE="citizenship_load_test.py"
HOST="http://localhost:8000"
USERS="17"  # Total de usuários (10 CitizenTestUser + 5 AtestadoTestUser + 2 ReportTestUser)
SPAWN_RATE="3.5"  # Taxa de spawn (2 + 1 + 0.5)
DURATION="5m"  # 5 minutos
REPORT_DIR="reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Cria diretório de relatórios se não existir
mkdir -p "$REPORT_DIR"

echo "🚀 Iniciando testes de performance para o módulo Citizenship..."
echo "📊 Usuários: $USERS"
echo "⏱️  Duração: $DURATION"
echo "📂 Diretório de relatórios: $REPORT_DIR"

# Executa o teste
locust -f "$LOCUSTFILE" /
  --host="$HOST" /
  --headless /
  --users="$USERS" /
  --spawn-rate="$SPAWN_RATE" /
  --run-time="$DURATION" /
  --csv="$REPORT_DIR/performance_$TIMESTAMP" /
  --html="$REPORT_DIR/performance_report_$TIMESTAMP.html"

# Verifica se o teste foi executado com sucesso
if [ $? -eq 0 ]; then
  echo "✅ Testes de performance concluídos com sucesso!"
  echo "📊 Relatório gerado em: $REPORT_DIR/performance_report_$TIMESTAMP.html"
else
  echo "❌ Ocorreu um erro durante a execução dos testes."
  exit 1
fi

