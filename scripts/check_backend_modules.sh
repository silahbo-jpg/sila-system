#!/bin/bash

BASE_DIR="backend/app/modules"
EXPECTED_FILES=("crud.py" "models.py" "schemas.py")
EXPECTED_DIRS=("routes" "tests")

echo "🔎 Verificando estrutura dos módulos em $BASE_DIR..."

for module in "$BASE_DIR"/*; do
    [ -d "$module" ] || continue
    echo "📁 Módulo: $(basename "$module")"

    for file in "${EXPECTED_FILES[@]}"; do
        if [ ! -f "$module/$file" ]; then
            echo "  ❌ Faltando arquivo: $file"
        fi
    done

    for dir in "${EXPECTED_DIRS[@]}"; do
        if [ ! -d "$module/$dir" ] && [ ! -f "$module/$dir.py" ]; then
            echo "  ❌ Faltando diretório ou arquivo: $dir"
        fi
    done
done 
