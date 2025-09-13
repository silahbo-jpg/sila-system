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

