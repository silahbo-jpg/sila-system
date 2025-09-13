#!/bin/bash

MODULES_DIR="backend/app/modules"
FRONTEND_SERVICES="frontend/webapp/src/services"

echo "🔎 Verificando arquivos de serviço no frontend para os módulos..."

for module in "$MODULES_DIR"/*; do
    [ -d "$module" ] || continue
    name=$(basename "$module")
    if [ ! -f "$FRONTEND_SERVICES/$name.ts" ] && [ ! -f "$FRONTEND_SERVICES/$name.tsx" ]; then
        echo "❌ Módulo '$name' não possui arquivo de serviço em '$FRONTEND_SERVICES'"
    fi
done 
