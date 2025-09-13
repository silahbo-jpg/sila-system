#!/bin/bash

# Script de deploy para ambiente de produção do SILA
# Uso: ./deploy_producao.sh [tag_version]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Verificar se tag foi fornecida
if [ -z "$1" ]; then
  echo -e "${YELLOW}Nenhuma tag específica fornecida. Usando 'latest'.${NC}"
  TAG="latest"
else
  TAG="$1"
  echo -e "${GREEN}Usando tag: $TAG${NC}"
fi

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${YELLOW}Iniciando deploy para produção...${NC}"

# Verificar se estamos no branch correto
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
  echo -e "${RED}ATENÇÃO: Você não está no branch main/master!${NC}"
  echo -e "${YELLOW}Branch atual: $CURRENT_BRANCH${NC}"
  read -p "Deseja continuar mesmo assim? (s/N): " CONTINUE
  if [ "$CONTINUE" != "s" ] && [ "$CONTINUE" != "S" ]; then
    echo -e "${RED}Deploy cancelado.${NC}"
    exit 1
  fi
fi

# Verificar se há alterações não commitadas
if ! git diff-index --quiet HEAD --; then
  echo -e "${RED}ATENÇÃO: Existem alterações não commitadas!${NC}"
  git status --short
  read -p "Deseja continuar mesmo assim? (s/N): " CONTINUE
  if [ "$CONTINUE" != "s" ] && [ "$CONTINUE" != "S" ]; then
    echo -e "${RED}Deploy cancelado.${NC}"
    exit 1
  fi
fi

# Construir imagens Docker
echo -e "${YELLOW}Construindo imagens Docker...${NC}"
docker-compose -f docker-compose.prod.yml build

# Aplicar tag às imagens
echo -e "${YELLOW}Aplicando tag às imagens: $TAG${NC}"
docker tag sila-backend:latest sila-backend:$TAG
docker tag sila-frontend:latest sila-frontend:$TAG

# Parar serviços atuais
echo -e "${YELLOW}Parando serviços atuais...${NC}"
docker-compose -f docker-compose.prod.yml down

# Iniciar novos serviços
echo -e "${YELLOW}Iniciando novos serviços...${NC}"
TAG=$TAG docker-compose -f docker-compose.prod.yml up -d

# Verificar status dos serviços
echo -e "${YELLOW}Verificando status dos serviços...${NC}"
docker-compose -f docker-compose.prod.yml ps

# Executar migrações do banco de dados
echo -e "${YELLOW}Executando migrações do banco de dados...${NC}"
docker-compose -f docker-compose.prod.yml exec backend python -m prisma migrate deploy

# Verificar logs para garantir que tudo está funcionando
echo -e "${YELLOW}Verificando logs do backend...${NC}"
docker-compose -f docker-compose.prod.yml logs --tail=50 backend

echo -e "${GREEN}Deploy para produção concluído com sucesso!${NC}"
echo -e "${GREEN}Versão: $TAG${NC}"

# Registrar o deploy no log
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deploy para produção - Tag: $TAG" >> deploy_history.log

exit 0
