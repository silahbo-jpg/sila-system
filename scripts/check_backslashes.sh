#!/bin/bash

echo "🔍 Verificando barras invertidas..."

FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|sh|ps1|yaml|yml|json|md)$' | while read -r file; do
    if grep -q '\\' "$file"; then
        echo "$file"
    fi
done)

if [ -n "$FILES" ]; then
    echo "❌ Erro: Foram encontradas barras invertidas ('\\') nos seguintes arquivos:"
    echo "$FILES"
    echo "\nPor favor, use barras normais (/) para caminhos de arquivo."
    exit 1
fi

exit 0

