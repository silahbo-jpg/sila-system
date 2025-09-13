# Makefile para o Projeto SILA System
# Comandos disponíveis: make <comando>

# Cores para saída colorida
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# Lista de comandos disponíveis
TARGET_MAX_CHAR_NUM=20

## Mostra esta ajuda
help:
	@echo ''
	@echo 'Comandos disponíveis:'
	@echo ''
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
	helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u
	@echo ''

# ======================
# Configuração do Projeto
# ======================

## Instala as dependências do projeto
install:
	@echo "${GREEN}Instalando dependências...${RESET}"
	pip install -r requirements.txt
	cd frontend && npm install

## Configura a estrutura do projeto
setup-project:
	@echo "${GREEN}Configurando estrutura do projeto...${RESET}"
	python scripts/create_modules.py

## Instala os hooks do pre-commit
install-hooks:
	@echo "${GREEN}Instalando hooks do pre-commit...${RESET}"
	pre-commit install

# ======================
# Testing
# ======================

## Run all tests with coverage and reports
test: clean-test-reports
	@echo "${GREEN}Running all tests with coverage...${RESET}"
	python -m scripts.run_tests --verbose

## Run tests in parallel (faster)
test-parallel: clean-test-reports
	@echo "${GREEN}Running tests in parallel...${RESET}"
	python -m scripts.run_tests --verbose --no-parallel

## Run a specific test file
test-file: clean-test-reports
	@if [ -z "$(file)" ]; then \
		echo "${YELLOW}Usage: make test-file file=path/to/test_file.py${RESET}"; \
		exit 1; \
	fi
	@echo "${GREEN}Running tests in $(file)...${RESET}"
	python -m scripts.run_tests --verbose $(file)

## Run tests with specific marker
test-mark: clean-test-reports
	@if [ -z "$(marker)" ]; then \
		echo "${YELLOW}Usage: make test-mark marker=marker_name${RESET}"; \
		echo "${YELLOW}Available markers: unit, integration, e2e, db, slow${RESET}"; \
		exit 1; \
	fi
	@echo "${GREEN}Running tests with marker '$(marker)'...${RESET}"
	python -m scripts.run_tests --verbose -m $(marker)

## Run only failed tests from last run
test-failed: clean-test-reports
	@echo "${GREEN}Running previously failed tests...${RESET}"
	python -m scripts.run_tests --verbose --last-failed

## Run tests with coverage report
coverage: clean-test-reports
	@echo "${GREEN}Generating coverage report...${RESET}"
	python -m scripts.run_tests --no-cov-report=term --cov-report=html
	@echo "${GREEN}Coverage report available at: file://$(shell pwd)/reports/coverage/index.html${RESET}"

## Clean test reports and cache
clean-test-reports:
	@echo "${YELLOW}Cleaning test reports and cache...${RESET}"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '.pytest_cache' -exec rm -rf {} +
	@rm -rf .coverage .coverage.* htmlcov/ reports/
	@mkdir -p reports/coverage

## Run linting and type checking
lint:
	@echo "${GREEN}Running linters...${RESET}"
	@echo "${YELLOW}Running flake8...${RESET}"
	flake8 app tests
	@echo "${YELLOW}Running black...${RESET}"
	black --check app tests
	@echo "${YELLOW}Running isort...${RESET}"
	isort --check-only --diff app tests
	@echo "${YELLOW}Running mypy...${RESET}"
	mypy app tests

## Format code with black and isort
format:
	@echo "${GREEN}Formatting code...${RESET}"
	black app tests
	isort app tests

## Run security checks
security:
	@echo "${GREEN}Running security checks...${RESET}"
	@echo "${YELLOW}Running bandit...${RESET}"
	bandit -r app -c pyproject.toml
	@echo "${YELLOW}Running safety...${RESET}"
	safety check --full-report

## Run all checks (lint, test, security)
check: lint test security
	@echo "${GREEN}All checks passed!${RESET}"

# ======================
# Docker

## Run all tests with coverage
.PHONY: test
test:
	@echo "${GREEN}Running tests with coverage...${RESET}"
	pytest -v --cov=app --cov-report=term-missing --cov-report=html:reports/coverage --junitxml=reports/junit.xml

## Run tests in watch mode (requires pytest-watch)
.PHONY: test-watch
test-watch:
	@echo "${GREEN}Watching for file changes to run tests...${RESET}"
	ptw -- -v --cov=app --cov-report=term-missing

## Run tests in parallel
.PHONY: test-parallel
test-parallel:
	@echo "${GREEN}Running tests in parallel...${RESET}"
	pytest -n auto -v --cov=app --cov-report=term-missing

## Run a specific test file
.PHONY: test-file
test-file:
	@echo "${GREEN}Running tests in $(file)...${RESET}"
	pytest -v $(file) -v --cov=app --cov-append

## Run tests in Docker
.PHONY: test-docker
test-docker:
	@echo "${GREEN}Running tests in Docker...${RESET}"
	docker-compose -f docker-compose.test.yml up --build --exit-code-from test-runner

## Generate coverage report
.PHONY: coverage
coverage:
	@echo "${GREEN}Generating coverage report...${RESET}"
	pytest --cov=app --cov-report=html:reports/coverage

## Run linting and type checking
.PHONY: lint
lint:
	@echo "${GREEN}Running linting...${RESET}"
	flake8 app tests
	mypy app tests

# ======================
# Backend
# ======================

## Inicia o servidor de desenvolvimento do backend
backend-run:
	@echo "${GREEN}Iniciando servidor de desenvolvimento...${RESET}"
	uvicorn backend.main:app --reload

## Executa os testes do backend
test-backend:
	@echo "${GREEN}Executando testes do backend...${RESET}"
	pytest backend/tests/

## Executa migrações do banco de dados
migrate:
	@echo "${GREEN}Executando migrações...${RESET}"
	alembic upgrade head

# ======================
# Frontend
# ======================

## Inicia o servidor de desenvolvimento do frontend
frontend-dev:
	@echo "${GREEN}Iniciando servidor de desenvolvimento do frontend...${RESET}"
	cd frontend && npm run dev

## Constrói o frontend para produção
frontend-build:
	@echo "${GREEN}Construindo frontend para produção...${RESET}"
	cd frontend && npm run build

# ======================
# Qualidade de Código
# ======================

## Executa a verificação de estilo e formatação
lint:
	@echo "${GREEN}Executando verificações de estilo...${RESET}"
	pre-commit run --all-files

## Formata o código automaticamente
format:
	@echo "${GREEN}Formatando código...${RESET}"
	black .
	isort .

## Uniformiza as variáveis de ambiente
uniformizar:
	@echo "${YELLOW}🔧 Executando uniformização institucional de senha nos .env...${RESET}"
	@python scripts/uniformizar_senha_envs.py
	@echo "${GREEN}✅ Processo concluído. Verifique o log em log_uniformizacao_envs.txt${RESET}"

## Verifica barras invertidas manualmente
check-backslashes:
	@echo "${YELLOW}🔍 Verificando barras invertidas...${RESET}"
	@! grep -r "\\" --include="*.py" --include="*.sh" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.md" . | grep -v "venv" | grep -v "node_modules"

# ======================
# CI/CD
# ======================

## Executa todas as verificações de CI/CD
ci: lint check-backslashes test-backend
	@echo "${GREEN}✅ Verificações de qualidade concluídas com sucesso!${RESET}"

## Sanitize and validate the entire project
sanitize:
	chmod +x scripts/sanitize.sh
	./scripts/sanitize.sh

## Run CI sanitization
ci_sanitize: sanitize
	@echo "✅ CI sanitization passed - project is clean"

.PHONY: validate_no_sqlite ci_validation sanitize ci_sanitize

# ======================
# Sanitization & Audit
# ======================

## Run comprehensive sanitization and audit
sanitize_audit:
	chmod +x scripts/sanitize_and_audit.sh
	./scripts/sanitize_and_audit.sh

## Check if system is production ready
production_ready: sanitize_audit
	@echo "✅ Production validation passed - system is clean and operational"

# ======================
# Utilitários
# ======================

## Limpa arquivos temporários
clean:
	@echo "${YELLOW}Limpando arquivos temporários...${RESET}"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

## Deploy backend with complete validation
deploy:
	chmod +x scripts/deploy_backend.sh
	./scripts/deploy_backend.sh

## Deploy backend on Windows
deploy_win:
	powershell -ExecutionPolicy Bypass -File scripts/deploy_backend.ps1

## Validate deployment by checking critical endpoints
validate_deployment:
	curl -f http://localhost:8000/health && \
	curl -f http://localhost:8000/api/protocols && \
	echo "✅ Deployment validated"

## Validate that no SQLite references exist in the codebase
validate_no_sqlite:
	chmod +x scripts/validate_no_sqlite.sh
	./scripts/validate_no_sqlite.sh

## Run CI validation including SQLite check
ci_validation: validate_no_sqlite
	@echo "✅ CI validation passed - no SQLite detected"

## Mostra o status do ambiente
status:
	@echo "${GREEN}=== Status do Ambiente ===${RESET}"
	@echo "Python: $(shell python --version 2>/dev/null || echo 'Não instalado')"
	@echo "Node: $(shell node --version 2>/dev/null || echo 'Não instalado')"
	@echo "npm: $(shell npm --version 2>/dev/null || echo 'Não instalado')"
	@echo "${GREEN}=========================${RESET}"
