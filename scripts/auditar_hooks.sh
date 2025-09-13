#!/bin/bash
# Caminho: scripts/auditar_hooks.sh
# Finalidade: Auditar alterações no .pre-commit-config.yaml com exportação institucional

set -e

# Diretório raiz do projeto
ROOT_DIR="C:/Users/User5/Music/MEGA1/sila/sila-system"
cd "$ROOT_DIR"

# Timestamp institucional
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Arquivos de saída
MD_LOG="logs/hooks_diff_$TIMESTAMP.md"
CSV_LOG="logs/hooks_diff_$TIMESTAMP.csv"

# Garante que o diretório de logs existe
mkdir -p logs

# Gera o diff e exporta para Markdown
echo "# Diff do .pre-commit-config.yaml ($TIMESTAMP)" > "$MD_LOG"
git diff .pre-commit-config.yaml >> "$MD_LOG"

# Gera CSV com versão antiga e nova (simplificado)
echo "Hook,Repositório,Versão Anterior,Versão Nova" > "$CSV_LOG"
grep -E 'repo:|rev:' .pre-commit-config.yaml | paste - - | sed 's/repo: //;s/rev: //' | awk -F'\t' '{print NR","$1","$2}' >> "$CSV_LOG"

# Simulação segura opcional
echo -e "\n🔍 Executando pre-commit em modo DryRun...\n"
pre-commit run --all-files --show-diff-on-failure || echo "⚠️ DryRun detectou falhas"

echo -e "\n✅ Auditoria concluída. Artefatos gerados:\n- $MD_LOG\n- $CSV_LOG"
