#!/bin/bash

MODULES_DIR="backend/app/modules"
FRONTEND_PAGES="frontend/webapp/src/pages"

echo "🔎 Verificando páginas no frontend para cada módulo do backend..."

for module in "$MODULES_DIR"/*; do
    [ -d "$module" ] || continue
    name=$(basename "$module")
    if [ ! -d "$FRONTEND_PAGES/$name" ] && [ ! -f "$FRONTEND_PAGES/$name.tsx" ]; then
        echo "❌ Módulo '$name' não possui página no frontend."
    fi
done 
