#!/bin/bash

# Script para executar testes com cobertura e gerar relatórios

# Ativa o ambiente virtual (se estiver usando)
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Instala dependências de teste
pip install -r requirements-test.txt

# Remove relatórios antigos
rm -rf htmlcov/
rm -f .coverage

# Executa os testes com cobertura
echo "Executando testes com cobertura..."
python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html:htmlcov

# Verifica se os testes passaram
if [ $? -eq 0 ]; then
    echo "✅ Testes concluídos com sucesso!"
    
    # Abre o relatório de cobertura no navegador (Linux/Unix)
    if command -v xdg-open > /dev/null; then
        xdg-open htmlcov/index.html
    # macOS
    elif command -v open > /dev/null; then
        open htmlcov/index.html
    fi
else
    echo "❌ Alguns testes falharam. Verifique os logs acima."
    exit 1
fi

