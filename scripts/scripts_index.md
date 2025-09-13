# SILA-System Scripts Documentation

Generated on: 2025-08-26 21:00:18

## Overview

This document provides an overview of all scripts in the SILA-System project.
Scripts are organized by category to support development, testing, and automation.

## Table of Contents

- [Archived](#archived) (3 scripts)
- [Backups](#backups) (61 scripts)
- [CI/CD Integration](#cicd-integration) (2 scripts)
- [Database Management](#database-management) (2 scripts)
- [Development Tools](#development-tools) (2 scripts)
- [Legacy Scripts](#legacy-scripts) (4 scripts)
- [Root Scripts](#root-scripts) (106 scripts)
- [Scripts](#scripts) (3 scripts)
- [Security & Audit](#security-&-audit) (2 scripts)
- [Tests](#tests) (3 scripts)
- [Utilities](#utilities) (2 scripts)

## Archived

### clean_project.py

**Path:** `archived\clean_project.py`
**Size:** 10.0 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### fix_and_migrate.ps1

**Path:** `archived\fix_and_migrate.ps1`
**Size:** 4.6 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### migrate_sqlite_to_postgres.py

**Path:** `archived\migrate_sqlite_to_postgres.py`
**Size:** 8.9 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

## Backups

### add_new_service.py

**Path:** `backups\standardize_20250817_075359\add_new_service.py`
**Size:** 6.4 KB
**Modified:** 2025-08-17

**Description:** Script para adicionar um novo serviço ao SILA

Este script facilita a criação de novos serviços no sistema SILA,
gerando a estrutura básica de arquivos e código necessários.

**Dependencies:**
- argparse
- os
- pathlib
- shutil
- sys

---

### analyze_migration.py

**Path:** `backups\standardize_20250817_075359\analyze_migration.py`
**Size:** 7.4 KB
**Modified:** 2025-08-17

**Description:** Script para análise e documentação da migração de django-backend para backend FastAPI.

Este script gera um relatório detalhado comparando os diretórios e arquivos entre
o django-backend e o backend F...

**Dependencies:**
- datetime
- json
- os
- pathlib

---

### audit_saude_refs.py

**Path:** `backups\standardize_20250817_075359\audit_saude_refs.py`
**Size:** 1.5 KB
**Modified:** 2025-08-17

**Description:** Script de auditoria para encontrar referências ao módulo 'saude' no projeto.

**Dependencies:**
- os
- pathlib
- re

---

### auditar-log-padronizacao.ps1

**Path:** `backups\standardize_20250817_075359\auditar-log-padronizacao.ps1`
**Size:** 1.7 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_binary_packages.py

**Path:** `backups\standardize_20250817_075359\check_binary_packages.py`
**Size:** 691.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- os
- pkg_resources
- sys

---

### check_no_sqlite.ps1

**Path:** `backups\standardize_20250817_075359\check_no_sqlite.ps1`
**Size:** 1.6 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### clean-temp.ps1

**Path:** `backups\standardize_20250817_075359\clean-temp.ps1`
**Size:** 643.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### clean_project.py

**Path:** `backups\standardize_20250817_075359\archived\clean_project.py`
**Size:** 10.0 KB
**Modified:** 2025-08-17

**Description:** Script para saneamento do projeto SILA
Este script implementa as recomendações de limpeza do projeto
baseadas na análise de inconsistências e problemas de portabilidade.

**Dependencies:**
- glob
- os
- shutil
- sys

---

### clean_python_cache.ps1

**Path:** `backups\standardize_20250817_075359\clean_python_cache.ps1`
**Size:** 8.2 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### convert_shell_to_powershell.ps1

**Path:** `backups\standardize_20250817_075359\convert_shell_to_powershell.ps1`
**Size:** 7.7 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### create_modules.py

**Path:** `backups\standardize_20250817_075359\create_modules.py`
**Size:** 6.0 KB
**Modified:** 2025-08-17

**Description:** SILA System - Create Module Structure

**Dependencies:**
- os
- pathlib

---

### detect_corrupted_scripts.py

**Path:** `backups\standardize_20250817_075359\detect_corrupted_scripts.py`
**Size:** 837.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- os
- py_compile

---

### fix-all.ps1

**Path:** `backups\standardize_20250817_075359\fix-all.ps1`
**Size:** 2.8 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-corrupted-content.py

**Path:** `backups\standardize_20250817_075359\fix-corrupted-content.py`
**Size:** 1.5 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- os
- pathlib

---

### fix-corrupted-filenames.ps1

**Path:** `backups\standardize_20250817_075359\fix-corrupted-filenames.ps1`
**Size:** 922.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-critical-filenames.py

**Path:** `backups\standardize_20250817_075359\scripts\fix-critical-filenames.py`
**Size:** 1.4 KB
**Modified:** 2025-08-21

**Description:** Corrige nomes de arquivos críticos corrompidos no projeto postgres.
Foca nos arquivos com 'nnn' ou 'otif' no nome.

**Dependencies:**
- os
- pathlib

---

### fix-migration-issues.ps1

**Path:** `backups\standardize_20250817_075359\fix-migration-issues.ps1`
**Size:** 5.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-notification-files.py

**Path:** `backups\standardize_20250817_075359\fix-notification-files.py`
**Size:** 1.8 KB
**Modified:** 2025-08-17

**Description:** Corrige os 6 arquivos com nomes corrompidos relacionados a notificações.
Executa renomeação segura com feedback claro.

**Dependencies:**
- os
- pathlib

---

### fix-sqlalchemy-refs.py

**Path:** `backups\standardize_20250817_075359\fix-sqlalchemy-refs.py`
**Size:** 2.3 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- os
- pathlib
- re

---

### fix-syntax-errors.py

**Path:** `backups\standardize_20250817_075359\fix-syntax-errors.py`
**Size:** 3.2 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- os
- pathlib
- re

---

### fix_and_migrate.ps1

**Path:** `backups\standardize_20250817_075359\archived\fix_and_migrate.ps1`
**Size:** 4.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix_database_urls.ps1

**Path:** `backups\standardize_20250817_075359\fix_database_urls.ps1`
**Size:** 990.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix_module_structure.ps1

**Path:** `backups\standardize_20250817_075359\fix_module_structure.ps1`
**Size:** 11.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix_module_structure_fixed.ps1

**Path:** `backups\standardize_20250817_075359\fix_module_structure_fixed.ps1`
**Size:** 10.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix_unterminated_strings.py

**Path:** `backups\standardize_20250817_075359\fix_unterminated_strings.py`
**Size:** 1.9 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- os
- pathlib

---

### generate-docs.ps1

**Path:** `backups\standardize_20250817_075359\generate-docs.ps1`
**Size:** 25.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate-index.ps1

**Path:** `backups\standardize_20250817_075359\generate-index.ps1`
**Size:** 1.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate-migration-report.py

**Path:** `backups\standardize_20250817_075359\generate-migration-report.py`
**Size:** 5.7 KB
**Modified:** 2025-08-17

**Description:** Script para gerar relatório de mapeamento da migração SQLAlchemy → Prisma

Este script analisa os modelos SQLAlchemy e Prisma e gera um relatório
detalhado do mapeamento entre eles, útil para document...

**Dependencies:**
- argparse
- datetime
- json
- os
- pathlib
- re
- sys
- typing

---

### generate-script-index.ps1

**Path:** `backups\standardize_20250817_075359\generate-script-index.ps1`
**Size:** 1.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate_script_index.py

**Path:** `backups\standardize_20250817_075359\generate_script_index.py`
**Size:** 8.2 KB
**Modified:** 2025-08-17

**Description:** ÍNDICE TÉCNICO DE SCRIPTS — Projeto SILA
Gera um índice completo de todos os scripts (.py, .ps1, .sh) do projeto,
classificando por tipo, módulo e status (válido, corrompido, ignorado).

**Dependencies:**
- collections
- datetime
- os
- re
- sys
- time

---

### master-migration.ps1

**Path:** `backups\standardize_20250817_075359\master-migration.ps1`
**Size:** 7.2 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### migrate-sqla-to-prisma.ps1

**Path:** `backups\standardize_20250817_075359\migrate-sqla-to-prisma.ps1`
**Size:** 2.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### migrate_data.py

**Path:** `backups\standardize_20250817_075359\migrate_data.py`
**Size:** 15.1 KB
**Modified:** 2025-08-17

**Description:** Script para migrar dados do banco SQLite legado para o novo esquema Prisma.

**Dependencies:**
- bcrypt
- datetime
- hashlib
- logging
- os
- pathlib
- secrets
- sqlite3

---

### migrate_django_to_fastapi.py

**Path:** `backups\standardize_20250817_075359\migrate_django_to_fastapi.py`
**Size:** 5.3 KB
**Modified:** 2025-08-17

**Description:** Script para migrar dados do Django SQLite para o novo esquema FastAPI + SQLAlchemy.

**Dependencies:**
- app.models.user
- datetime
- logging
- os
- pathlib
- sqlalchemy
- sqlalchemy.orm
- sqlite3
- sys
- typing

---

### migrate_django_to_sqlalchemy.py

**Path:** `backups\standardize_20250817_075359\migrate_django_to_sqlalchemy.py`
**Size:** 1.0 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- django
- old_django_app.models
- os
- sqlalchemy
- sqlalchemy.orm
- your_fastapi_app.models

---

### migrate_sqlite_to_postgres.py

**Path:** `backups\standardize_20250817_075359\archived\migrate_sqlite_to_postgres.py`
**Size:** 8.2 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### migrate_users.py

**Path:** `backups\standardize_20250817_075359\migrate_users.py`
**Size:** 4.5 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- bcrypt
- datetime
- hashlib
- logging
- sqlite3
- sys

---

### module_validator.py

**Path:** `backups\standardize_20250817_075359\module_validator.py`
**Size:** 20.9 KB
**Modified:** 2025-08-17

**Description:** Módulo de validação de módulos do sistema SILA.

Este script verifica a integridade e completude dos módulos do projeto,
validando estrutura de arquivos, implementação de código, rotas da API e testes...

**Dependencies:**
- argparse
- ast
- csv
- dataclasses
- enum
- importlib
- io
- json
- os
- pathlib

---

### move_obsolete_scripts.ps1

**Path:** `backups\standardize_20250817_075359\move_obsolete_scripts.ps1`
**Size:** 1.7 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### post-migration-audit.ps1

**Path:** `backups\standardize_20250817_075359\post-migration-audit.ps1`
**Size:** 2.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### prisma-migrate-core.py

**Path:** `backups\standardize_20250817_075359\prisma-migrate-core.py`
**Size:** 4.9 KB
**Modified:** 2025-08-17

**Description:** Script para migrar automaticamente modelos SQLAlchemy para Prisma

Este script identifica modelos SQLAlchemy, extrai suas estruturas e
gera o equivalente em Prisma schema, além de converter serviços.

**Dependencies:**
- argparse
- os
- pathlib
- re
- sys
- typing

---

### recreate-critical-files.py

**Path:** `backups\standardize_20250817_075359\recreate-critical-files.py`
**Size:** 4.9 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- os
- pathlib

---

### restore_notification_filenames.py

**Path:** `backups\standardize_20250817_075359\restore_notification_filenames.py`
**Size:** 4.1 KB
**Modified:** 2025-08-17

**Description:** Script para restaurar nomes corrompidos de arquivos de notificação.
Cria backups antes de fazer quaisquer alterações e processa apenas arquivos existentes.

**Dependencies:**
- datetime
- os
- pathlib
- shutil
- sys
- typing

---

### restore_original_filenames.py

**Path:** `backups\standardize_20250817_075359\restore_original_filenames.py`
**Size:** 2.4 KB
**Modified:** 2025-08-17

**Description:** Restore Original Filenames Script

This script restores the original filenames of files that were previously
renamed by the fix-corrupted-filenames.ps1 script.

**Dependencies:**
- os
- pathlib
- re
- sys

---

### rollback-prisma-migration.ps1

**Path:** `backups\standardize_20250817_075359\rollback-prisma-migration.ps1`
**Size:** 3.8 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### run_all_validations.ps1

**Path:** `backups\standardize_20250817_075359\run_all_validations.ps1`
**Size:** 16.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### setup_env.ps1

**Path:** `backups\standardize_20250817_075359\setup_env.ps1`
**Size:** 2.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### setup_modules.py

**Path:** `backups\standardize_20250817_075359\setup_modules.py`
**Size:** 5.8 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### setup_project_structure.py

**Path:** `backups\standardize_20250817_075359\setup_project_structure.py`
**Size:** 6.8 KB
**Modified:** 2025-08-17

**Description:** SILA System - Project Structure Setup Script

This script automates the creation of required module files and directories.

**Dependencies:**
- os
- pathlib

---

### setup_structure.py

**Path:** `backups\standardize_20250817_075359\setup_structure.py`
**Size:** 7.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### sila_migrate.py

**Path:** `backups\standardize_20250817_075359\sila_migrate.py`
**Size:** 14.1 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- argparse
- bcrypt
- datetime
- email.mime.multipart
- email.mime.text
- hashlib
- logging
- os
- smtplib
- sqlite3

---

### standardize-config.ps1

**Path:** `backups\standardize_20250817_075359\standardize-config.ps1`
**Size:** 6.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### sync-endpoints.ps1

**Path:** `backups\standardize_20250817_075359\sync-endpoints.ps1`
**Size:** 16.2 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### test_environment.py

**Path:** `backups\standardize_20250817_075359\test_environment.py`
**Size:** 2.1 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- importlib
- logging
- os
- pathlib
- psycopg2
- sys

---

### validate-module-integrity.ps1

**Path:** `backups\standardize_20250817_075359\validate-module-integrity.ps1`
**Size:** 14.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### validate-module-integrity.py

**Path:** `backups\standardize_20250817_075359\validate-module-integrity.py`
**Size:** 16.6 KB
**Modified:** 2025-08-17

**Description:** Validador de Integridade de Módulos do SILA

Este script consolida várias verificações de integridade em uma única ferramenta:
- Validação de sintaxe Python (usando py_compile)
- Verificação de padrõe...

**Dependencies:**
- ast
- concurrent.futures
- dataclasses
- datetime
- enum
- logging
- os
- pathlib
- py_compile
- re

---

### validate-modules.ps1

**Path:** `backups\standardize_20250817_075359\validate-modules.ps1`
**Size:** 8.1 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### validate-py-compile.ps1

**Path:** `backups\standardize_20250817_075359\validate-py-compile.ps1`
**Size:** 1.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### validate-syntax.py

**Path:** `backups\standardize_20250817_075359\validate-syntax.py`
**Size:** 796.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- ast
- os
- pathlib

---

### validate_py_compile.py

**Path:** `backups\standardize_20250817_075359\validate_py_compile.py`
**Size:** 9.2 KB
**Modified:** 2025-08-17

**Description:** Script para validar todos os arquivos Python do projeto usando py_compile
e gerar um log detalhado de sucesso ou erro, além de um relatório de validação.

**Dependencies:**
- argparse
- concurrent.futures
- datetime
- logging
- os
- py_compile
- sys
- time

---

### validate_py_syntax.py

**Path:** `backups\standardize_20250817_075359\validate_py_syntax.py`
**Size:** 2.4 KB
**Modified:** 2025-08-17

**Description:** Valida a sintaxe de todos os arquivos Python do projeto.

**Dependencies:**
- ast
- pathlib
- sys

---

## CI/CD Integration

### run_tests.py

**Path:** `ci\run_tests.py`
**Size:** 4.9 KB
**Modified:** 2025-08-22

**Description:** Test runner script for SILA System.

This script provides a consistent way to run tests with proper configuration
and reporting. It can be used both locally and in CI environments.

**Dependencies:**
- argparse
- json
- os
- pathlib
- pybadges
- shutil
- subprocess
- sys
- typing

---

### validate_py_syntax.py

**Path:** `ci\validate_py_syntax.py`
**Size:** 2.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

## Database Management

### check_db_connection.py

**Path:** `db_new\check_db_connection.py`
**Size:** 1.0 KB
**Modified:** 2025-08-18

**Description:** No description available

**Dependencies:**
- datetime
- dotenv
- os
- psycopg2

---

### setup_database.py

**Path:** `db_new\setup_database.py`
**Size:** 3.8 KB
**Modified:** 2025-08-26

**Description:** Database Setup Script
Sets up PostgreSQL database and runs Alembic migrations.

**Dependencies:**
- app.core.config
- app.db.session
- os
- pathlib
- subprocess
- sys

---

## Development Tools

### create_superuser.py

**Path:** `dev\create_superuser.py`
**Size:** 2.2 KB
**Modified:** 2025-08-26

**Description:** Create Superuser Script
Creates an administrative user for the SILA-System.

**Dependencies:**
- app.core.config
- app.core.security
- app.crud.user
- app.db.session
- app.schemas.user
- getpass
- os
- pathlib
- sys

---

### setup_dev.py

**Path:** `dev\setup_dev.py`
**Size:** 3.3 KB
**Modified:** 2025-08-26

**Description:** Development Environment Setup Script
Sets up the complete development environment for SILA-System.

**Dependencies:**
- os
- pathlib
- scripts.db.setup_database
- shutil
- subprocess
- sys

---

## Legacy Scripts

### migrate_django_to_fastapi.py

**Path:** `legacy\archived\migrate_django_to_fastapi.py`
**Size:** 5.5 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### migrate_django_to_sqlalchemy.py

**Path:** `legacy\archived\migrate_django_to_sqlalchemy.py`
**Size:** 1.1 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### project-closure.ps1

**Path:** `legacy\archived\project-closure.ps1`
**Size:** 3.8 KB
**Modified:** 2025-08-18

**Description:** PowerShell script

---

### validate-syntax.py

**Path:** `legacy\archived\validate-syntax.py`
**Size:** 823.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

## Root Scripts

### add_new_service.py

**Path:** `add_new_service.py`
**Size:** 6.5 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### analyze-project-structure.ps1

**Path:** `analyze-project-structure.ps1`
**Size:** 4.4 KB
**Modified:** 2025-08-19

**Description:** PowerShell script

---

### analyze_and_migrate.ps1

**Path:** `analyze_and_migrate.ps1`
**Size:** 4.1 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### analyze_migration.py

**Path:** `analyze_migration.py`
**Size:** 7.5 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### analyze_project.ps1

**Path:** `analyze_project.ps1`
**Size:** 4.6 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### audit-project.ps1

**Path:** `audit-project.ps1`
**Size:** 6.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### audit_modules.ps1

**Path:** `audit_modules.ps1`
**Size:** 4.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### audit_saude_refs.py

**Path:** `audit_saude_refs.py`
**Size:** 1.6 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### auditar-log-padronizacao.ps1

**Path:** `auditar-log-padronizacao.ps1`
**Size:** 1.7 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### batch_generate_services.py

**Path:** `batch_generate_services.py`
**Size:** 4.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- argparse
- csv
- os
- pathlib
- subprocess

---

### check_and_generate_modules.py

**Path:** `check_and_generate_modules.py`
**Size:** 7.5 KB
**Modified:** 2025-08-17

**Description:** Script para verificar e preencher automaticamente módulos que estão faltando componentes.
Baseado na estrutura do módulo 'citizenship' como referência.

**Dependencies:**
- os
- pathlib
- re
- shutil
- sys
- traceback
- typing

---

### check_backend_modules.ps1

**Path:** `check_backend_modules.ps1`
**Size:** 1.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_backend_tests.ps1

**Path:** `check_backend_tests.ps1`
**Size:** 1.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_backslashes.ps1

**Path:** `check_backslashes.ps1`
**Size:** 1.1 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_binary_packages.py

**Path:** `check_binary_packages.py`
**Size:** 777.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### check_credentials.py

**Path:** `check_credentials.py`
**Size:** 3.7 KB
**Modified:** 2025-08-22

**Description:** Check for credential policy violations.

This script scans the codebase for any credentials that don't match the allowed patterns.

**Dependencies:**
- os
- pathlib
- re
- sys
- typing

---

### check_db_connection.py

**Path:** `check_db_connection.py`
**Size:** 1.0 KB
**Modified:** 2025-08-18

**Description:** No description available

**Dependencies:**
- datetime
- dotenv
- os
- psycopg2

---

### check_env.ps1

**Path:** `check_env.ps1`
**Size:** 268.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_frontend_pages.ps1

**Path:** `check_frontend_pages.ps1`
**Size:** 1.1 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_frontend_services.ps1

**Path:** `check_frontend_services.ps1`
**Size:** 1.1 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_home_dir.ps1

**Path:** `check_home_dir.ps1`
**Size:** 1.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### check_module_integrity.py

**Path:** `check_module_integrity.py`
**Size:** 6.0 KB
**Modified:** 2025-08-17

**Description:** Script para verificar a integridade dos módulos do backend.

**Dependencies:**
- os
- pathlib
- sys
- traceback
- typing

---

### check_no_sqlite.ps1

**Path:** `check_no_sqlite.ps1`
**Size:** 1.6 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### clean-temp.ps1

**Path:** `clean-temp.ps1`
**Size:** 670.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### clean_python_cache.ps1

**Path:** `clean_python_cache.ps1`
**Size:** 8.2 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### cleanup.ps1

**Path:** `cleanup.ps1`
**Size:** 2.2 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### convert_shell_to_powershell.ps1

**Path:** `convert_shell_to_powershell.ps1`
**Size:** 7.7 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### create_modules.py

**Path:** `create_modules.py`
**Size:** 6.2 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### detect_corrupted_scripts.py

**Path:** `detect_corrupted_scripts.py`
**Size:** 864.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### fix-all.ps1

**Path:** `fix-all.ps1`
**Size:** 3.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-corrupted-content.py

**Path:** `fix-corrupted-content.py`
**Size:** 1.5 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### fix-corrupted-filenames.ps1

**Path:** `fix-corrupted-filenames.ps1`
**Size:** 960.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-imports.ps1

**Path:** `fix-imports.ps1`
**Size:** 1.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-migration-issues.ps1

**Path:** `fix-migration-issues.ps1`
**Size:** 5.6 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-notification-files.py

**Path:** `fix-notification-files.py`
**Size:** 1.8 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### fix-project.ps1

**Path:** `fix-project.ps1`
**Size:** 1.1 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix-sqlalchemy-refs.py

**Path:** `fix-sqlalchemy-refs.py`
**Size:** 2.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### fix-syntax-errors.py

**Path:** `fix-syntax-errors.py`
**Size:** 3.2 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### fix_database_urls.ps1

**Path:** `fix_database_urls.ps1`
**Size:** 1.2 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix_encoding.py

**Path:** `fix_encoding.py`
**Size:** 582.0 B
**Modified:** 2025-08-19

**Description:** No description available

**Dependencies:**
- csv
- pathlib

---

### fix_module_structure.ps1

**Path:** `fix_module_structure.ps1`
**Size:** 11.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix_module_structure_fixed.ps1

**Path:** `fix_module_structure_fixed.ps1`
**Size:** 10.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fix_syntax_errors_targeted.py

**Path:** `fix_syntax_errors_targeted.py`
**Size:** 9.3 KB
**Modified:** 2025-08-17

**Description:** Script para correção automatizada de erros de sintaxe específicos em arquivos Python.

Este script analisa e corrige erros de sintaxe em arquivos específicos do projeto,
focando nas linhas indicadas e...

**Dependencies:**
- logging
- os
- pathlib
- py_compile
- re
- sys

---

### fix_unterminated_strings.py

**Path:** `fix_unterminated_strings.py`
**Size:** 1.9 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### fixed_encoding.ps1

**Path:** `fixed_encoding.ps1`
**Size:** 7.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fixed_init.ps1

**Path:** `fixed_init.ps1`
**Size:** 4.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fixed_init_project.ps1

**Path:** `fixed_init_project.ps1`
**Size:** 4.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### fixed_script.ps1

**Path:** `fixed_script.ps1`
**Size:** 7.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate-docs.ps1

**Path:** `generate-docs.ps1`
**Size:** 25.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate-index.ps1

**Path:** `generate-index.ps1`
**Size:** 2.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate-migration-report.py

**Path:** `generate-migration-report.py`
**Size:** 5.7 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### generate-requirements.ps1

**Path:** `generate-requirements.ps1`
**Size:** 2.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate-script-index.ps1

**Path:** `generate-script-index.ps1`
**Size:** 2.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### generate-scripts-index.ps1

**Path:** `generate-scripts-index.ps1`
**Size:** 598.0 B
**Modified:** 2025-08-19

**Description:** PowerShell script

---

### generate_script_index.py

**Path:** `generate_script_index.py`
**Size:** 7.8 KB
**Modified:** 2025-08-26

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### generate_service.py

**Path:** `generate_service.py`
**Size:** 9.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- os
- pathlib
- sys

---

### init_project.ps1

**Path:** `init_project.ps1`
**Size:** 5.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### init_project_simple.ps1

**Path:** `init_project_simple.ps1`
**Size:** 7.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### log_hook_execution.py

**Path:** `log_hook_execution.py`
**Size:** 3.2 KB
**Modified:** 2025-08-19

**Description:** Logger institucional para execução de hooks pre-commit.

Registra:
- ID e tipo do hook
- Arquivos afetados
- Tempo de execução
- Saída e erros do comando
- Log com timestamp em logs/hooks_exec_YYYY-MM...

**Dependencies:**
- datetime
- logging
- os
- subprocess
- sys
- time
- typing

---

### main.py

**Path:** `main.py`
**Size:** 1.4 KB
**Modified:** 2025-08-26

**Description:** No description available

**Dependencies:**
- click
- scripts.audit.audit_secrets
- scripts.audit.validate_env
- scripts.ci.run_tests
- scripts.db.check_connection
- scripts.db.setup_database
- scripts.dev.create_superuser
- scripts.utils.fix_imports
- scripts.utils.generate_openapi_client
- scripts.utils.tree_modules

---

### master-migration.ps1

**Path:** `master-migration.ps1`
**Size:** 7.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### migrate-sqla-to-prisma.ps1

**Path:** `migrate-sqla-to-prisma.ps1`
**Size:** 2.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### migrate_data.py

**Path:** `migrate_data.py`
**Size:** 16.6 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### migrate_users.py

**Path:** `migrate_users.py`
**Size:** 5.3 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### module_validator.py

**Path:** `module_validator.py`
**Size:** 24.5 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### move_obsolete_scripts.ps1

**Path:** `move_obsolete_scripts.ps1`
**Size:** 1.8 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### organize-python-files.ps1

**Path:** `organize-python-files.ps1`
**Size:** 3.1 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### organize_backend.ps1

**Path:** `organize_backend.ps1`
**Size:** 5.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### padronizar_envs.py

**Path:** `padronizar_envs.py`
**Size:** 1.9 KB
**Modified:** 2025-08-19

**Description:** No description available

**Dependencies:**
- csv
- datetime
- dotenv
- os

---

### post-migration-audit.ps1

**Path:** `post-migration-audit.ps1`
**Size:** 2.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### preencher_env_critico.py

**Path:** `preencher_env_critico.py`
**Size:** 1.6 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- datetime
- dotenv
- pathlib
- sys

---

### preencher_env_critico_multi.py

**Path:** `preencher_env_critico_multi.py`
**Size:** 2.2 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- argparse
- datetime
- os

---

### preencher_env_critico_multi_csv.py

**Path:** `preencher_env_critico_multi_csv.py`
**Size:** 2.8 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- argparse
- csv
- datetime
- os

---

### prisma-migrate-core.py

**Path:** `prisma-migrate-core.py`
**Size:** 4.9 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### quick_check.py

**Path:** `quick_check.py`
**Size:** 406.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- sys

---

### recreate-critical-files.py

**Path:** `recreate-critical-files.py`
**Size:** 5.0 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### restore_notification_filenames.py

**Path:** `restore_notification_filenames.py`
**Size:** 4.2 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### restore_original_filenames.py

**Path:** `restore_original_filenames.py`
**Size:** 2.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### rollback-prisma-migration.ps1

**Path:** `rollback-prisma-migration.ps1`
**Size:** 3.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### run_all_validations.ps1

**Path:** `run_all_validations.ps1`
**Size:** 17.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### run_integration_example.py

**Path:** `run_integration_example.py`
**Size:** 1005.0 B
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- asyncio
- backend.app.modules.integration.examples.integration_example
- logging
- os
- sys

---

### run_tests.py

**Path:** `run_tests.py`
**Size:** 4.9 KB
**Modified:** 2025-08-22

**Description:** Test runner script for SILA System.

This script provides a consistent way to run tests with proper configuration
and reporting. It can be used both locally and in CI environments.

**Dependencies:**
- argparse
- json
- os
- pathlib
- pybadges
- shutil
- subprocess
- sys
- typing

---

### setup_env.ps1

**Path:** `setup_env.ps1`
**Size:** 3.0 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### setup_modules.py

**Path:** `setup_modules.py`
**Size:** 6.0 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### setup_project_structure.py

**Path:** `setup_project_structure.py`
**Size:** 7.0 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### setup_structure.py

**Path:** `setup_structure.py`
**Size:** 7.7 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### sila_migrate.py

**Path:** `sila_migrate.py`
**Size:** 15.3 KB
**Modified:** 2025-08-21

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### simple_init.ps1

**Path:** `simple_init.ps1`
**Size:** 2.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### simple_test.ps1

**Path:** `simple_test.ps1`
**Size:** 101.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### standardize-config.ps1

**Path:** `standardize-config.ps1`
**Size:** 7.9 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### sync-endpoints.ps1

**Path:** `sync-endpoints.ps1`
**Size:** 16.2 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### temp_script.ps1

**Path:** `temp_script.ps1`
**Size:** 9.7 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### test_execution.ps1

**Path:** `test_execution.ps1`
**Size:** 204.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### testar_ligacoes_envs.py

**Path:** `testar_ligacoes_envs.py`
**Size:** 1.6 KB
**Modified:** 2025-08-19

**Description:** No description available

**Dependencies:**
- csv
- datetime
- dotenv
- os
- psycopg2

---

### uniformizar_senha_envs.py

**Path:** `uniformizar_senha_envs.py`
**Size:** 3.3 KB
**Modified:** 2025-08-20

**Description:** No description available

**Dependencies:**
- datetime
- os
- re
- sys

---

### update_gitignore.ps1

**Path:** `update_gitignore.ps1`
**Size:** 595.0 B
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### validar_env_conexao.py

**Path:** `validar_env_conexao.py`
**Size:** 1.7 KB
**Modified:** 2025-08-19

**Description:** No description available

**Dependencies:**
- csv
- datetime
- dotenv
- os
- psycopg2

---

### validar_env_conexao_precommit.py

**Path:** `validar_env_conexao_precommit.py`
**Size:** 1.0 KB
**Modified:** 2025-08-19

**Description:** No description available

**Dependencies:**
- dotenv
- os
- sys

---

### validar_env_critico.py

**Path:** `validar_env_critico.py`
**Size:** 1.3 KB
**Modified:** 2025-08-18

**Description:** No description available

**Dependencies:**
- datetime
- dotenv
- pathlib

---

### validate-module-integrity.ps1

**Path:** `validate-module-integrity.ps1`
**Size:** 16.6 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### validate-module-integrity.py

**Path:** `validate-module-integrity.py`
**Size:** 18.7 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### validate-modules.ps1

**Path:** `validate-modules.ps1`
**Size:** 8.5 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### validate-py-compile.ps1

**Path:** `validate-py-compile.ps1`
**Size:** 1.4 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### validate_csv.py

**Path:** `validate_csv.py`
**Size:** 4.5 KB
**Modified:** 2025-08-19

**Description:** Validação institucional de arquivos CSV para pre-commit.

Valida:
- Encoding UTF-8 (abrindo diretamente em UTF-8; chardet só auxilia)
- Delimitador permitido (vírgula, ponto e vírgula, tab)
- Cabeçalh...

**Dependencies:**
- chardet
- csv
- datetime
- os
- pathlib
- sys
- typing

---

### validate_py_compile.py

**Path:** `validate_py_compile.py`
**Size:** 9.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### validate_py_syntax.py

**Path:** `validate_py_syntax.py`
**Size:** 2.4 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

## Scripts

### fix-critical-filenames.py

**Path:** `scripts\fix-critical-filenames.py`
**Size:** 1.5 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### init_project_final.ps1

**Path:** `scripts\init_project_final.ps1`
**Size:** 4.3 KB
**Modified:** 2025-08-17

**Description:** PowerShell script

---

### reset_test_db.ps1

**Path:** `scripts\reset_test_db.ps1`
**Size:** 1.8 KB
**Modified:** 2025-08-18

**Description:** PowerShell script

---

## Security & Audit

### check_credentials.py

**Path:** `audit_new\check_credentials.py`
**Size:** 3.7 KB
**Modified:** 2025-08-22

**Description:** Check for credential policy violations.

This script scans the codebase for any credentials that don't match the allowed patterns.

**Dependencies:**
- os
- pathlib
- re
- sys
- typing

---

### validate_env.py

**Path:** `audit_new\validate_env.py`
**Size:** 5.4 KB
**Modified:** 2025-08-26

**Description:** Environment Validation Script
Validates .env files for security and completeness.

**Dependencies:**
- os
- pathlib
- re
- sys
- typing

---

## Tests

### generate_tests.py

**Path:** `tests\generate_tests.py`
**Size:** 7.8 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

### generate_tests_simple.py

**Path:** `tests\generate_tests_simple.py`
**Size:** 7.5 KB
**Modified:** 2025-08-17

**Description:** Script simplificado para gerar testes básicos para os módulos do backend.

**Dependencies:**
- os
- pathlib
- sys
- traceback
- typing

---

### test_environment.py

**Path:** `tests\test_environment.py`
**Size:** 2.1 KB
**Modified:** 2025-08-17

**Description:** No description available

**Dependencies:**
- (parse error: SyntaxError)

---

## Utilities

### fix_imports.py

**Path:** `utils_new\fix_imports.py`
**Size:** 7.1 KB
**Modified:** 2025-08-26

**Description:** Import Standardization Script
Fixes and standardizes Python imports across the project.

**Dependencies:**
- ast
- os
- pathlib
- re
- sys
- typing

---

### tree_modules.py

**Path:** `utils_new\tree_modules.py`
**Size:** 2.8 KB
**Modified:** 2025-08-26

**Description:** Module Tree Visualization Script
Generates a clean tree structure of the modules directory.

**Dependencies:**
- os
- pathlib
- sys

---
