# Etapa base
FROM python:3.11-slim

# Configuração básica
WORKDIR /app

# Instala dependências do sistema (Prisma client Python precisa do Node)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Prisma CLI globalmente (para migrations e generate)
RUN npm install -g prisma

# Copiar código do backend
COPY . .

# Gerar cliente Prisma
RUN prisma generate || true

# Porta exposta
EXPOSE 8000

# Comando default (substituído pelo docker-compose com --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
