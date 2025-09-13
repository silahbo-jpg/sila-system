#!/bin/bash

# Caminhos base
BASE_DIR="backend/app/modules"
TESTS_DIR="tests/modules"
FRONTEND_PAGES="frontend/webapp/src/pages"
FRONTEND_SERVICES="frontend/webapp/src/services"
ROUTES_FILE="backend/app/main.py"

# Arquivos esperados
EXPECTED_FILES=("crud.py" "models.py" "schemas.py")
EXPECTED_DIRS=("routes" "tests")

# Cabeçalho do relatório
REPORT_MD="audit_report.md"
REPORT_CSV="audit_report.csv"
echo "| Módulo | CRUD | Schemas | Models | Rotas | Testes | Página FE | Serviço FE | Funções CRUD | Funções Teste | Status |" > "$REPORT_MD"
echo "|--------|------|---------|--------|-------|--------|-----------|------------|--------------|--------------|--------|" >> "$REPORT_MD"
echo "Modulo,CRUD,SCHEMAS,MODELS,ROTAS,TESTES,PAGINA_FE,SERVICO_FE,FUNCOES_CRUD,FUNCOES_TESTE,STATUS" > "$REPORT_CSV"

for module in "$BASE_DIR"/*; do
    [ -d "$module" ] || continue
    name=$(basename "$module")
    status="✔️"

    # Inicializa arrays para armazenar status
    declare -A file_status
    declare -A dir_status
    
    # Verifica presença dos arquivos
    for file in "${EXPECTED_FILES[@]}"; do
        file_status["$file"]="❌"
        [ -f "$module/$file" ] && file_status["$file"]="✔️"
    done

    # Verifica presença dos diretórios
    for dir in "${EXPECTED_DIRS[@]}"; do
        dir_status["$dir"]="❌"
        { [ -d "$module/$dir" ] || [ -f "$module/$dir.py" ]; } && dir_status["$dir"]="✔️"
    done

    # Funções implementadas
    funcoes_crud="❌"
    if [ -f "$module/crud.py" ]; then
        grep -qE '^def |^class ' "$module/crud.py" && funcoes_crud="✔️"
    fi

    funcoes_teste="❌"
    if [ -d "$module/tests" ]; then
        grep -r -qE '^def test_' "$module/tests" && funcoes_teste="✔️"
    elif [ -f "$module/tests.py" ]; then
        grep -qE '^def test_' "$module/tests.py" && funcoes_teste="✔️"
    fi

    # Rotas expostas
    rotas="❌"
    grep -q "$name" "$ROUTES_FILE" && rotas="✔️"

    # Testes globais
    testes="❌"
    [ -d "$TESTS_DIR/$name" ] && testes="✔️"

    # Página frontend
    pagina_fe="❌"
    { [ -d "$FRONTEND_PAGES/$name" ] || [ -f "$FRONTEND_PAGES/$name.tsx" ]; } && pagina_fe="✔️"

    # Serviço frontend
    servico_fe="❌"
    { [ -f "$FRONTEND_SERVICES/$name.ts" ] || [ -f "$FRONTEND_SERVICES/$name.tsx" ]; } && servico_fe="✔️"

    # Status geral
    if [[ "${file_status[crud.py]}" == "❌" || "${file_status[schemas.py]}" == "❌" || "${file_status[models.py]}" == "❌" || "$rotas" == "❌" || "$testes" == "❌" || "$pagina_fe" == "❌" || "$servico_fe" == "❌" || "$funcoes_crud" == "❌" ]]; then
        status="⚠️ Parcial"
    fi

    # Relatório Markdown
    echo "| $name | ${file_status[crud.py]} | ${file_status[schemas.py]} | ${file_status[models.py]} | $rotas | $testes | $pagina_fe | $servico_fe | $funcoes_crud | $funcoes_teste | $status |" >> "$REPORT_MD"
    # Relatório CSV
    echo "$name,${file_status[crud.py]},${file_status[schemas.py]},${file_status[models.py]},$rotas,$testes,$pagina_fe,$servico_fe,$funcoes_crud,$funcoes_teste,$status" >> "$REPORT_CSV"
done

echo "/nRelatórios gerados: $REPORT_MD, $REPORT_CSV" 
