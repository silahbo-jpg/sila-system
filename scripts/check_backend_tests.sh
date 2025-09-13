#!/bin/bash

MODULES_DIR="backend/app/modules"
TESTS_DIR="tests/modules"

echo "🔎 Verificando se cada módulo tem pasta de testes..."

for module in "$MODULES_DIR"/*; do
    [ -d "$module" ] || continue
    name=$(basename "$module")
    if [ ! -d "$TESTS_DIR/$name" ]; then
        echo "❌ Módulo '$name' não possui testes em '$TESTS_DIR/$name'"
    fi
done 
