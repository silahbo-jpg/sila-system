# Etapa de build
FROM node:18-alpine as build

WORKDIR /app

# Instala dependências
COPY package*.json ./
RUN npm ci

# Copia o código fonte e faz o build
COPY . .
RUN npm run build

# Etapa de produção
FROM nginx:alpine

# Copia os arquivos de build para o nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copia a configuração personalizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expõe a porta 80
EXPOSE 80

# Inicia o nginx
CMD ["nginx", "-g", "daemon off;"]
