# SILA - Sistema Integrado de Licenciamento e Autorizações

Sistema integrado para gestão de licenciamentos e autorizações municipais.

## 🚀 Estrutura do Projeto

```
.
├── backend/               # Backend FastAPI
│   ├── core/             # Módulos principais
│   ├── api/              # Endpoints da API
│   ├── services/         # Lógica de negócios
│   ├── models/           # Modelos de dados
│   ├── utils/            # Utilitários e helpers
│   └── tests/            # Testes automatizados
│
├── frontend/             # Aplicação frontend
│   ├── webapp/           # Aplicação web
│   └── mobileapp/        # Aplicativo móvel
│
├── docs/                 # Documentação
├── scripts/              # Scripts úteis
├── certificados/         # Certificados e chaves
├── binarios/             # Arquivos binários
└── logs/                 # Arquivos de log
```

## 🛠️ Configuração do Ambiente

### Pré-requisitos

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Docker (opcional, para desenvolvimento)

### Configuração Inicial

1. **Clonar o repositório**
   ```bash
   git clone <repo-url>
   cd postgres
   ```

2. **Configurar ambiente Python**
   ```bash
   # Criar e ativar ambiente virtual
   python -m venv venv
   .\venv\Scripts\activate

   # Instalar dependências
   pip install -r requirements.txt
   ```

3. **Configurar variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Editar o arquivo .env com as configurações necessárias
   ```

4. **Inicializar banco de dados**
   ```bash
   # Aplicar migrações
   alembic upgrade head
   
   # Carregar dados iniciais (se necessário)
   python -m scripts.load_initial_data
   ```

5. **Iniciar o servidor de desenvolvimento**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=app tests/

# Verificar estilo de código
flake8 .
black --check .
```

## 🚀 Implantação

Consulte o guia de [implantação](scripts/DEPLOYMENT.md) para instruções detalhadas sobre como implantar o sistema com validação automática.

Comandos disponíveis:
```bash
# Linux/Mac
make deploy

# Windows
make deploy_win

# Validar implantação
make validate_deployment
```

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, leia nosso [guia de contribuição](CONTRIBUTING.md) para obter detalhes sobre nosso código de conduta e o processo para enviar solicitações pull.

## 📞 Suporte

Para suporte, entre em contato com a equipe de desenvolvimento ou abra uma issue no repositório.

Sistema modular para digitalização de serviços das administrações municipais, comunais e distritos urbanos de Angola.

## 🚫 SQLite Removido

**ATENÇÃO**: O suporte a SQLite foi completamente removido deste projeto. O sistema agora utiliza exclusivamente PostgreSQL como banco de dados.

### O que foi feito:
- Removidos todos os arquivos `.db` e backups relacionados ao SQLite
- Desativado o script `init_db.py` que criava o banco SQLite
- Adicionada verificação automática para bloquear commits que contenham referências a SQLite
- Atualizadas as configurações para usar apenas PostgreSQL

### Como proceder:
1. Certifique-se de ter o Docker instalado e em execução
2. Use o comando `docker-compose up -d db` para subir o container do PostgreSQL
3. As migrações serão aplicadas automaticamente

### Verificações de segurança:
- O pre-commit inclui um hook que bloqueia qualquer referência a SQLite
- O sistema não iniciará se detectar configurações de SQLite
- Todas as referências antigas foram removidas do código-fonte

## ⚠️ Importante: Diretório 'home'

O diretório `home/` foi removido intencionalmente e **não deve ser recriado**. Este diretório estava causando problemas no projeto e foi removido como parte da reestruturação.

### Medidas de Prevenção

1. **Arquivo `.gitkeep`**: Contém avisos explicando que o diretório não deve ser recriado.
2. **Teste Automatizado**: O teste `test_directory_structure.py` verifica se o diretório foi recriado acidentalmente.
3. **Git Hooks**: Um script de pré-commit impede o commit acidental do diretório.
4. **Regras no `.gitignore`**: O diretório é explicitamente ignorado, exceto pelo arquivo `.gitkeep`.

Se você encontrar o diretório `home/` sendo recriado, verifique:
- Manipuladores de upload de arquivos
- Configurações de armazenamento
- Middleware que possa estar criando diretórios automaticamente

## Componentes
- Backend: FastAPI
- Frontend Web: React + Tailwind
- App Mobile: React Native
- DevOps: Docker + Nginx + Scripts

## Como usar

### Configuração Rápida

#### Backend
```powershell
# Na pasta backend
.\setup_backend.ps1
```
Este script irá:
1. Ativar o ambiente virtual (ou criar se não existir)
2. Criar o arquivo .env com configurações básicas (se não existir)
3. Instalar as dependências do projeto
4. Gerar o cliente Prisma
5. Verificar a conexão com o PostgreSQL
6. Iniciar o servidor Uvicorn

#### Usando Docker (Alternativa)
```bash
docker-compose up --build
```

Depois acesse:
- Web: http://localhost:3000/
- API: http://localhost:8000/

## Configuração no Windows

### Pré-requisitos
- Python 3.10 ou superior
- PostgreSQL 14 ou superior
- Docker Desktop para Windows
- Git para Windows

### Passos para configuração

1. **Clone o repositório**
   ```powershell
   git clone https://github.com/seu-usuario/postgres.git
   cd postgres
   ```

2. **Crie e ative um ambiente virtual**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências**
   ```powershell
   pip install --force-reinstall -r requirements.txt
   ```

4. **Verifique o ambiente**
   ```powershell
   python .\scripts\test_environment.py
   ```

5. **Inicie o PostgreSQL via Docker**
   ```powershell
   docker-compose up -d db
   ```

6. **Execute o backend**
   ```powershell
   cd backend
   uvicorn app.main:app --reload
   ```

7. **Em outro terminal, execute o frontend**
   ```powershell
   cd frontend
   npm install
   npm start
   ```

### Solução de problemas no Windows

Se encontrar problemas com pacotes binários, execute:
```powershell
python .\scripts\check_binary_packages.py
```

Para limpar arquivos de cache e corrigir problemas comuns:
```powershell
.\sanear_projeto.bat
```

### 🔧 Correção de Strings Não Terminadas

O script `scripts/fix_unterminated_strings.py` corrige automaticamente docstrings mal formatadas na primeira linha de arquivos `__init__.py`.

- Detecta aspas duplas não terminadas
- Aplica correção apenas em arquivos do projeto (exclui `.venv`)
- Integrado ao `fix-all.ps1` e `aplicar_correcoes.bat`
- Gera log em `logs/correcoes_strings.txt`

## Executando Testes

Para executar os testes de estrutura de diretórios:

```bash
cd backend
pytest ../tests/test_directory_structure.py -v
```

