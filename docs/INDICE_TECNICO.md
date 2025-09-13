# 📦 Índice Técnico de Scripts — Projeto SILA

*Gerado em: 2025-08-15 07:59:07*

**Total de scripts encontrados: 532**
**Válidos: 524** | **Corrompidos: 8**

## 📊 Distribuição por Tipo

| Tipo | Quantidade |
|------|------------|
| Other | 351 |
| Test | 77 |
| Audit | 27 |
| Fix | 15 |
| Migration | 15 |
| Generate | 14 |
| Setup | 12 |
| Validator | 9 |
| Cleanup | 3 |
| Utility | 1 |

## 🧨 Arquivos com Nomes Corrompidos

| Arquivo | Caminho | Problema |
|---------|-------|----------|
| `nnnotifications.py` | `backend\app\api\routes\nnnotifications.py` | ⚠️ Nome corrompido: `otifications` → `notifications` |
| `nnotificador.py` | `backend\app\core\nnotificador.py` | ⚠️ Nome corrompido: `otifica` → `notifica` |
| `nnnnotificacoes.py` | `backend\app\services\nnnnotificacoes.py` | ⚠️ Nome corrompido: `otificacoes` → `notificacoes` |
| `nnnotifications.py` | `backend\app\services\nnnotifications.py` | ⚠️ Nome corrompido: `otifications` → `notifications` |
| `nnotification_service.py` | `backend\app\services\nnotification_service.py` | ⚠️ Nome corrompido: `otifica` → `notifica` |
| `test_nnnotifications.py` | `backend\tests\test_nnnotifications.py` | ⚠️ Nome corrompido: `otifications` → `notifications` |
| `fix-nnnotification-files.py` | `scripts\fix-nnnotification-files.py` | ⚠️ Nome corrompido: `otifica` → `notifica` |
| `restore_nnotification_filenames.py` | `scripts\restore_nnotification_filenames.py` | ⚠️ Nome corrompido: `otifica` → `notifica` |

## 🛠️ Scripts Válidos por Módulo

### Agendamentos

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\appointments\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\appointments\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\appointments\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\appointments\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\appointments\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\appointments\__init__.py` |
| `crud.py` | Other | `backend\app\modules\appointments\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\appointments\endpoints.py` |
| `models.py` | Other | `backend\app\modules\appointments\models.py` |
| `schemas.py` | Other | `backend\app\modules\appointments\schemas.py` |
| `services.py` | Other | `backend\app\modules\appointments\services.py` |
| `test_appointments.py` | Test | `tests\modules\appointments\test_appointments.py` |

### App

| Script | Tipo | Caminho |
|--------|------|-------|
| `test_auth.py` | Test | `backend\tests\modules\app\test_auth.py` |
| `test_citizen.py` | Test | `backend\tests\modules\app\test_citizen.py` |
| `test_crud.py` | Test | `backend\tests\modules\app\test_crud.py` |
| `test_endpoints.py` | Test | `backend\tests\modules\app\test_endpoints.py` |
| `test_protected.py` | Test | `backend\tests\modules\app\test_protected.py` |
| `test_schemas.py` | Test | `backend\tests\modules\app\test_schemas.py` |
| `test_services.py` | Test | `backend\tests\modules\app\test_services.py` |

### Autenticação

| Script | Tipo | Caminho |
|--------|------|-------|
| `security.py` | Other | `backend\app\auth\security.py` |

### Banco de Dados

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\db\__init__.py` |
| `base.py` | Other | `backend\app\db\base.py` |
| `base.py` | Other | `backend\app\db\repositories\base.py` |
| `database.py` | Other | `backend\app\db\database.py` |
| `user.py` | Other | `backend\app\db\repositories\user.py` |

### CRUD

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\crud\__init__.py` |
| `base.py` | Other | `backend\app\crud\base.py` |
| `crud_user.py` | Other | `backend\app\crud\crud_user.py` |

### Central de Serviços

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\service_hub\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\service_hub\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\service_hub\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\service_hub\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\service_hub\tests\__init__.py` |
| `crud.py` | Other | `backend\app\modules\service_hub\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\service_hub\endpoints.py` |
| `models.py` | Other | `backend\app\modules\service_hub\models.py` |
| `schemas.py` | Other | `backend\app\modules\service_hub\schemas.py` |
| `services.py` | Other | `backend\app\modules\service_hub\services.py` |
| `test_endpoints.py` | Test | `backend\app\modules\service_hub\tests\test_endpoints.py` |
| `test_services.py` | Test | `backend\app\modules\service_hub\tests\test_services.py` |

### Cidadania

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\citizenship\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\citizenship\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\citizenship\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\citizenship\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\citizenship\tests\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\citizenship\utils\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\citizenship\__init__.py` |
| `api.py` | Other | `backend\app\modules\citizenship\api.py` |
| `atualizacao_endereco.py` | Other | `backend\app\modules\citizenship\models\atualizacao_endereco.py` |
| `atualizacao_endereco.py` | Other | `backend\app\modules\citizenship\routes\atualizacao_endereco.py` |
| `atualizacao_endereco.py` | Other | `backend\app\modules\citizenship\schemas\atualizacao_endereco.py` |
| `conftest.py` | Other | `backend\tests\modules\citizenship\conftest.py` |
| `crud.py` | Other | `backend\app\modules\citizenship\crud.py` |
| `dependencies.py` | Other | `backend\app\modules\citizenship\dependencies.py` |
| `e2e_test.py` | Test | `backend\tests\modules\citizenship\e2e_test.py` |
| `emissao_b_i.py` | Other | `backend\app\modules\citizenship\models\emissao_b_i.py` |
| `emissao_b_i.py` | Other | `backend\app\modules\citizenship\routes\emissao_b_i.py` |
| `emissao_b_i.py` | Other | `backend\app\modules\citizenship\schemas\emissao_b_i.py` |
| `endpoints.py` | Other | `backend\app\modules\citizenship\endpoints.py` |
| `event_handlers.py` | Other | `backend\app\modules\citizenship\services\event_handlers.py` |
| `exceptions.py` | Other | `backend\app\modules\citizenship\exceptions.py` |
| `handlers.py` | Other | `backend\app\modules\citizenship\handlers.py` |
| `loaders.py` | Other | `backend\app\modules\citizenship\loaders.py` |
| `measure_coverage.py` | Other | `backend\tests\modules\citizenship\measure_coverage.py` |
| `models.py` | Other | `backend\app\modules\citizenship\models.py` |
| `permission_checker.py` | Other | `backend\app\modules\citizenship\utils\permission_checker.py` |
| `permissions.py` | Other | `backend\app\modules\citizenship\permissions.py` |
| `route_analyzer.py` | Other | `backend\app\modules\citizenship\utils\route_analyzer.py` |
| `run_e2e_tests.py` | Other | `backend\tests\modules\citizenship\run_e2e_tests.py` |
| `run_error_tests.py` | Other | `backend\tests\modules\citizenship\run_error_tests.py` |
| `run_integration_tests.py` | Other | `backend\tests\modules\citizenship\run_integration_tests.py` |
| `run_permission_tests_directly.py` | Other | `backend\tests\modules\citizenship\run_permission_tests_directly.py` |
| `schemas.py` | Other | `backend\app\modules\citizenship\schemas.py` |
| `services.py` | Other | `backend\app\modules\citizenship\services.py` |
| `test_citizenship.py` | Test | `tests\modules\citizenship\test_citizenship.py` |
| `test_citizenship_endpoints.py` | Test | `backend\tests\modules\citizenship\test_citizenship_endpoints.py` |
| `test_crud.py` | Test | `backend\tests\modules\citizenship\test_crud.py` |
| `test_endpoints.py` | Test | `tests\modules\citizenship\test_endpoints.py` |
| `test_error_scenarios.py` | Test | `backend\tests\modules\citizenship\test_error_scenarios.py` |
| `test_feedback_endpoints.py` | Test | `backend\tests\modules\citizenship\test_feedback_endpoints.py` |
| `test_feedback_service.py` | Test | `backend\tests\modules\citizenship\test_feedback_service.py` |
| `test_integration_endpoints.py` | Test | `backend\tests\modules\citizenship\test_integration_endpoints.py` |
| `test_permissions.py` | Test | `backend\tests\modules\citizenship\test_permissions.py` |
| `test_permissions_isolated.py` | Test | `backend\tests\modules\citizenship\test_permissions_isolated.py` |
| `test_schemas.py` | Test | `backend\tests\modules\citizenship\test_schemas.py` |
| `test_services.py` | Test | `backend\tests\modules\citizenship\test_services.py` |

### Comercial

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\commercial\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\commercial\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\commercial\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\commercial\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\commercial\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\commercial\__init__.py` |
| `abertura_processo.py` | Other | `backend\app\modules\commercial\models\abertura_processo.py` |
| `abertura_processo.py` | Other | `backend\app\modules\commercial\routes\abertura_processo.py` |
| `abertura_processo.py` | Other | `backend\app\modules\commercial\schemas\abertura_processo.py` |
| `conftest.py` | Other | `backend\tests\modules\commercial\conftest.py` |
| `crud.py` | Other | `backend\app\modules\commercial\crud.py` |
| `deps.py` | Other | `backend\app\modules\commercial\deps.py` |
| `endpoints.py` | Other | `backend\app\modules\commercial\endpoints.py` |
| `models.py` | Other | `backend\app\modules\commercial\models.py` |
| `schemas.py` | Other | `backend\app\modules\commercial\schemas.py` |
| `services.py` | Other | `backend\app\modules\commercial\services.py` |
| `test_config.py` | Test | `backend\tests\modules\commercial\test_config.py` |
| `test_endpoints.py` | Test | `backend\tests\modules\commercial\test_endpoints.py` |
| `test_endpoints.py` | Test | `tests\modules\commercial\test_endpoints.py` |
| `test_isolated.py` | Test | `backend\tests\modules\commercial\test_isolated.py` |
| `test_schemas.py` | Test | `backend\tests\modules\commercial\test_schemas.py` |
| `test_services.py` | Test | `backend\tests\modules\commercial\test_services.py` |

### Common

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\common\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\common\__init__.py` |

### Complaints

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\complaints\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\complaints\__init__.py` |
| `conftest.py` | Other | `backend\app\modules\complaints\tests\conftest.py` |
| `conftest.py` | Other | `backend\tests\modules\complaints\conftest.py` |
| `test_config.py` | Test | `backend\tests\modules\complaints\test_config.py` |
| `test_endpoints.py` | Test | `backend\tests\modules\complaints\test_endpoints.py` |
| `test_isolated.py` | Test | `backend\tests\modules\complaints\test_isolated.py` |
| `test_isolated_endpoints.py` | Test | `backend\tests\modules\complaints\test_isolated_endpoints.py` |
| `test_service.py` | Test | `backend\tests\modules\complaints\test_service.py` |

### Core

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\core\__init__.py` |
| `__init__.py` | Other | `backend\app\core\db\__init__.py` |
| `auth_utils.py` | Other | `backend\app\core\auth_utils.py` |
| `cache.py` | Other | `backend\app\core\cache.py` |
| `config.py` | Other | `backend\app\core\config.py` |
| `deps.py` | Other | `backend\app\core\deps.py` |
| `event_setup.py` | Other | `backend\app\core\event_setup.py` |
| `exceptions.py` | Other | `backend\app\core\exceptions.py` |
| `formatters.py` | Other | `backend\app\core\formatters.py` |
| `logging.py` | Other | `backend\app\core\logging.py` |
| `logging_config.py` | Other | `backend\app\core\logging_config.py` |
| `middleware.py` | Other | `backend\app\core\middleware.py` |
| `permissions.py` | Other | `backend\app\core\permissions.py` |
| `regra_negocio.py` | Other | `backend\app\core\regra_negocio.py` |
| `regras_negocio.py` | Other | `backend\app\core\regras_negocio.py` |
| `responses.py` | Other | `backend\app\core\responses.py` |
| `scheduler.py` | Other | `backend\app\core\scheduler.py` |
| `security.py` | Other | `backend\app\core\security.py` |

### Documentos

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\documents\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\documents\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\documents\tests\__init__.py` |
| `document_service.py` | Other | `backend\app\modules\documents\services\document_service.py` |

### Educação

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\education\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\education\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\education\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\education\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\education\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\education\__init__.py` |
| `crud.py` | Other | `backend\app\modules\education\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\education\endpoints.py` |
| `matricula_escolar.py` | Other | `backend\app\modules\education\models\matricula_escolar.py` |
| `matricula_escolar.py` | Other | `backend\app\modules\education\routes\matricula_escolar.py` |
| `matricula_escolar.py` | Other | `backend\app\modules\education\schemas\matricula_escolar.py` |
| `models.py` | Other | `backend\app\modules\education\models.py` |
| `schemas.py` | Other | `backend\app\modules\education\schemas.py` |
| `services.py` | Other | `backend\app\modules\education\services.py` |
| `test_education.py` | Test | `tests\modules\education\test_education.py` |

### Endereços

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\address\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\address\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\address\tests\__init__.py` |
| `address_service.py` | Other | `backend\app\modules\address\services\address_service.py` |

### Esquemas

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\schemas\__init__.py` |
| `token.py` | Other | `backend\app\schemas\token.py` |
| `user.py` | Other | `backend\app\schemas\user.py` |

### Estatísticas

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\statistics\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\statistics\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\statistics\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\statistics\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\statistics\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\statistics\__init__.py` |
| `crud.py` | Other | `backend\app\modules\statistics\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\statistics\endpoints.py` |
| `models.py` | Other | `backend\app\modules\statistics\models.py` |
| `schemas.py` | Other | `backend\app\modules\statistics\schemas.py` |
| `services.py` | Other | `backend\app\modules\statistics\services.py` |
| `test_endpoints.py` | Test | `tests\modules\statistics\test_endpoints.py` |

### Finanças

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\finance\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\finance\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\finance\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\finance\schemas\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\finance\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\finance\tests\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\finance\utils\__init__.py` |
| `payment.py` | Other | `backend\app\modules\finance\models\payment.py` |
| `payment.py` | Other | `backend\app\modules\finance\services\payment.py` |
| `transaction.py` | Other | `backend\app\modules\finance\models\transaction.py` |

### Governança

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\governance\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\governance\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\governance\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\governance\schemas\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\governance\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\governance\tests\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\governance\utils\__init__.py` |
| `audit_log.py` | Audit | `backend\app\modules\governance\models\audit_log.py` |

### Integração

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\integration\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\integration\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\integration\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\integration\schemas\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\integration\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\integration\tests\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\integration\utils\__init__.py` |
| `bna_adapter.py` | Other | `backend\app\modules\integration\adapters\bna_adapter.py` |
| `event_routes.py` | Other | `backend\app\modules\integration\routes\event_routes.py` |
| `event_schemas.py` | Other | `backend\app\modules\integration\schemas\event_schemas.py` |
| `event_service.py` | Other | `backend\app\modules\integration\services\event_service.py` |
| `integration_event.py` | Other | `backend\app\modules\integration\models\integration_event.py` |
| `integration_example.py` | Other | `backend\app\modules\integration\examples\integration_example.py` |
| `integration_gateway.py` | Other | `backend\app\modules\integration\integration_gateway.py` |
| `simplifica_adapter.py` | Other | `backend\integration\adapters\simplifica_adapter.py` |
| `test_integration_gateway.py` | Test | `backend\app\modules\integration\tests\test_integration_gateway.py` |

### Interno

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\internal\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\internal\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\internal\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\internal\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\internal\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\internal\__init__.py` |
| `crud.py` | Other | `backend\app\modules\internal\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\internal\endpoints.py` |
| `models.py` | Other | `backend\app\modules\internal\models.py` |
| `schemas.py` | Other | `backend\app\modules\internal\schemas.py` |
| `services.py` | Other | `backend\app\modules\internal\services.py` |
| `test_internal.py` | Test | `tests\modules\internal\test_internal.py` |

### Justiça

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\justice\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\justice\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\justice\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\justice\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\justice\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\justice\__init__.py` |
| `crud.py` | Other | `backend\app\modules\justice\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\justice\endpoints.py` |
| `integrations.py` | Other | `backend\app\modules\justice\integrations.py` |
| `models.py` | Other | `backend\app\modules\justice\models.py` |
| `reports.py` | Other | `backend\app\modules\justice\reports.py` |
| `schemas.py` | Other | `backend\app\modules\justice\schemas.py` |
| `services.py` | Other | `backend\app\modules\justice\services.py` |
| `test_justice.py` | Test | `tests\modules\justice\test_justice.py` |

### Middleware

| Script | Tipo | Caminho |
|--------|------|-------|
| `audit_log.py` | Audit | `backend\app\middleware\audit_log.py` |
| `audit_middleware.py` | Audit | `backend\app\middleware\audit_middleware.py` |
| `error_handler.py` | Other | `backend\app\middleware\error_handler.py` |

### Modelos

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\common\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\complaints\models\__init__.py` |

### Registro Civil

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\registry\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\registry\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\registry\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\registry\schemas\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\registry\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\registry\tests\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\registry\utils\__init__.py` |
| `citizen.py` | Other | `backend\app\modules\registry\models\citizen.py` |

### Rotas

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\common\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\complaints\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\routers\__init__.py` |
| `api.py` | Other | `backend\app\routers\api.py` |
| `audit.py` | Audit | `backend\app\api\routes\audit.py` |
| `auth.py` | Other | `backend\app\api\routes\auth.py` |
| `auth.py` | Other | `backend\app\routers\auth.py` |
| `auth.py` | Other | `backend\app\routes\auth.py` |
| `auth_router.py` | Other | `backend\app\routes\auth_router.py` |
| `citizen.py` | Other | `backend\app\api\routes\citizen.py` |
| `dashboard.py` | Other | `backend\app\api\routes\dashboard.py` |
| `dashboard_v2.py` | Other | `backend\app\api\routes\dashboard_v2.py` |
| `debug_users.py` | Other | `backend\app\api\routes\debug_users.py` |
| `monitoring.py` | Other | `backend\app\api\routes\monitoring.py` |
| `municipe.py` | Other | `backend\app\api\routes\municipe.py` |
| `roles.py` | Other | `backend\app\api\routes\roles.py` |

### Saneamento

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\sanitation\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\sanitation\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\sanitation\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\sanitation\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\sanitation\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\sanitation\__init__.py` |
| `crud.py` | Other | `backend\app\modules\sanitation\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\sanitation\endpoints.py` |
| `models.py` | Other | `backend\app\modules\sanitation\models.py` |
| `schemas.py` | Other | `backend\app\modules\sanitation\schemas.py` |
| `services.py` | Other | `backend\app\modules\sanitation\services.py` |
| `test_endpoints.py` | Test | `tests\modules\sanitation\test_endpoints.py` |

### Saúde

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\health\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\health\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\health\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\health\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\health\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\health\__init__.py` |
| `agendamento_consulta.py` | Other | `backend\app\modules\health\models\agendamento_consulta.py` |
| `agendamento_consulta.py` | Other | `backend\app\modules\health\routes\agendamento_consulta.py` |
| `agendamento_consulta.py` | Other | `backend\app\modules\health\schemas\agendamento_consulta.py` |
| `agendamento_teleconsulta.py` | Other | `backend\app\modules\health\models\agendamento_teleconsulta.py` |
| `agendamento_teleconsulta.py` | Other | `backend\app\modules\health\routes\agendamento_teleconsulta.py` |
| `agendamento_teleconsulta.py` | Other | `backend\app\modules\health\schemas\agendamento_teleconsulta.py` |
| `conftest.py` | Other | `backend\tests\modules\health\conftest.py` |
| `crud.py` | Other | `backend\app\modules\health\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\health\endpoints.py` |
| `exceptions.py` | Other | `backend\app\modules\health\exceptions.py` |
| `handlers.py` | Other | `backend\app\modules\health\handlers.py` |
| `models.py` | Other | `backend\app\modules\health\models.py` |
| `schemas.py` | Other | `backend\app\modules\health\schemas.py` |
| `services.py` | Other | `backend\app\modules\health\services.py` |
| `setup.py` | Setup | `backend\app\modules\health\setup.py` |
| `solicitacao_exame.py` | Other | `backend\app\modules\health\models\solicitacao_exame.py` |
| `solicitacao_exame.py` | Other | `backend\app\modules\health\routes\solicitacao_exame.py` |
| `solicitacao_exame.py` | Other | `backend\app\modules\health\schemas\solicitacao_exame.py` |
| `test_endpoints.py` | Test | `backend\tests\modules\health\test_endpoints.py` |
| `test_health.py` | Test | `tests\modules\health\test_health.py` |
| `test_schemas.py` | Test | `backend\tests\modules\health\test_schemas.py` |
| `test_services.py` | Test | `backend\tests\modules\health\test_services.py` |

### Serviços

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\common\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\complaints\services\__init__.py` |
| `document_validation_metrics.py` | Other | `backend\app\services\document_validation_metrics.py` |
| `faturacao_api.py` | Other | `backend\app\services\faturacao_api.py` |
| `image_validator.py` | Validator | `backend\app\services\image_validator.py` |
| `monitoring.py` | Other | `backend\app\services\monitoring.py` |
| `permission_service.py` | Other | `backend\app\services\permission_service.py` |
| `qr_generator.py` | Other | `backend\app\services\qr_generator.py` |
| `user_service.py` | Other | `backend\app\services\user_service.py` |

### Social

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\social\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\social\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\social\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\social\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\social\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\social\__init__.py` |
| `crud.py` | Other | `backend\app\modules\social\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\social\endpoints.py` |
| `models.py` | Other | `backend\app\modules\social\models.py` |
| `schemas.py` | Other | `backend\app\modules\social\schemas.py` |
| `services.py` | Other | `backend\app\modules\social\services.py` |
| `test_social.py` | Test | `tests\modules\social\test_social.py` |

### Urbanismo

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\modules\urbanism\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\urbanism\models\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\urbanism\routes\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\urbanism\services\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\urbanism\tests\__init__.py` |
| `__init__.py` | Other | `backend\tests\modules\urbanism\__init__.py` |
| `crud.py` | Other | `backend\app\modules\urbanism\crud.py` |
| `endpoints.py` | Other | `backend\app\modules\urbanism\endpoints.py` |
| `licenca_construcao.py` | Other | `backend\app\modules\urbanism\models\licenca_construcao.py` |
| `licenca_construcao.py` | Other | `backend\app\modules\urbanism\routes\licenca_construcao.py` |
| `licenca_construcao.py` | Other | `backend\app\modules\urbanism\schemas\licenca_construcao.py` |
| `models.py` | Other | `backend\app\modules\urbanism\models.py` |
| `schemas.py` | Other | `backend\app\modules\urbanism\schemas.py` |
| `services.py` | Other | `backend\app\modules\urbanism\services.py` |

### Utilitários

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\tests\utils\__init__.py` |
| `dashboard_utils.py` | Other | `backend\app\api\utils\dashboard_utils.py` |
| `file_upload.py` | Other | `backend\app\utils\file_upload.py` |
| `geo_utils.py` | Other | `backend\app\utils\geo_utils.py` |
| `pdf_generator.py` | Other | `backend\app\utils\pdf_generator.py` |
| `qrcode_gen.py` | Other | `backend\app\utils\qrcode_gen.py` |
| `qrcode_generator.py` | Other | `backend\app\utils\qrcode_generator.py` |
| `utils.py` | Utility | `backend\tests\utils\utils.py` |
| `validador_foto.py` | Other | `backend\app\utils\validador_foto.py` |

### general

| Script | Tipo | Caminho |
|--------|------|-------|
| `__init__.py` | Other | `backend\app\__init__.py` |
| `__init__.py` | Other | `backend\app\api\v1\__init__.py` |
| `__init__.py` | Other | `backend\app\api\v1\endpoints\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\common\__init__.py` |
| `__init__.py` | Other | `backend\app\modules\complaints\__init__.py` |
| `__init__.py` | Other | `backend\tests\__init__.py` |
| `add_new_service.py` | Other | `scripts\add_new_service.py` |
| `analyze_migration.py` | Migration | `scripts\analyze_migration.py` |
| `audit_modules.ps1` | Audit | `scripts\audit_modules.ps1` |
| `audit_modules.sh` | Audit | `scripts\audit_modules.sh` |
| `audit_saude_refs.py` | Audit | `scripts\audit_saude_refs.py` |
| `auth.py` | Other | `backend\app\api\v1\endpoints\auth.py` |
| `auth_router.py` | Other | `backend\app\auth_router.py` |
| `auth_utils.py` | Other | `backend\app\auth_utils.py` |
| `base.py` | Other | `backend\app\api\v1\endpoints\base.py` |
| `batch_generate_services.py` | Other | `scripts\batch_generate_services.py` |
| `check_and_fix_locks.py` | Audit | `backend\scripts\check_and_fix_locks.py` |
| `check_and_generate_modules.py` | Audit | `scripts\check_and_generate_modules.py` |
| `check_and_repair_db.py` | Audit | `backend\check_and_repair_db.py` |
| `check_backend_modules.ps1` | Audit | `scripts\check_backend_modules.ps1` |
| `check_backend_modules.sh` | Audit | `scripts\check_backend_modules.sh` |
| `check_backend_tests.ps1` | Test | `scripts\check_backend_tests.ps1` |
| `check_backend_tests.sh` | Test | `scripts\check_backend_tests.sh` |
| `check_backslashes.ps1` | Audit | `scripts\check_backslashes.ps1` |
| `check_backslashes.sh` | Audit | `scripts\check_backslashes.sh` |
| `check_binary_packages.py` | Audit | `scripts\check_binary_packages.py` |
| `check_env.ps1` | Audit | `scripts\check_env.ps1` |
| `check_frontend_pages.ps1` | Audit | `scripts\check_frontend_pages.ps1` |
| `check_frontend_pages.sh` | Audit | `scripts\check_frontend_pages.sh` |
| `check_frontend_services.ps1` | Audit | `scripts\check_frontend_services.ps1` |
| `check_frontend_services.sh` | Audit | `scripts\check_frontend_services.sh` |
| `check_home_dir.ps1` | Audit | `scripts\check_home_dir.ps1` |
| `check_home_dir.sh` | Audit | `scripts\check_home_dir.sh` |
| `check_module_integrity.py` | Audit | `scripts\check_module_integrity.py` |
| `check_no_sqlite.ps1` | Audit | `scripts\check_no_sqlite.ps1` |
| `check_no_sqlite.sh` | Audit | `scripts\check_no_sqlite.sh` |
| `check_prisma.py` | Audit | `backend\check_prisma.py` |
| `check_sqlite_settings.py` | Audit | `backend\scripts\check_sqlite_settings.py` |
| `citizenship_load_test.py` | Test | `backend\tests\performance\citizenship_load_test.py` |
| `clean-temp.ps1` | Cleanup | `scripts\clean-temp.ps1` |
| `clean_project.py` | Cleanup | `scripts\archived\clean_project.py` |
| `clean_python_cache.ps1` | Cleanup | `scripts\clean_python_cache.ps1` |
| `compile_requirements.ps1` | Other | `backend\scripts\compile_requirements.ps1` |
| `config.py` | Other | `backend\tests\performance\config.py` |
| `conftest.py` | Other | `backend\app\tests\conftest.py` |
| `conftest.py` | Other | `backend\tests\conftest.py` |
| `conftest.py` | Other | `tests\conftest.py` |
| `convert_shell_to_powershell.ps1` | Other | `scripts\convert_shell_to_powershell.ps1` |
| `create_modules.py` | Generate | `scripts\create_modules.py` |
| `create_superuser.py` | Generate | `backend\create_superuser.py` |
| `create_superuser.py` | Generate | `backend\scripts\create_superuser.py` |
| `create_test.py` | Test | `backend\create_test.py` |
| `create_user.py` | Generate | `backend\create_user.py` |
| `crud.py` | Other | `backend\app\modules\common\crud.py` |
| `crud.py` | Other | `backend\app\modules\complaints\crud.py` |
| `deploy_producao.ps1` | Other | `devops\scripts\deploy_producao.ps1` |
| `deploy_producao.sh` | Other | `devops\scripts\deploy_producao.sh` |
| `deps.py` | Other | `backend\app\api\deps.py` |
| `detect_corrupted_scripts.py` | Other | `scripts\detect_corrupted_scripts.py` |
| `endpoints.py` | Other | `backend\app\modules\common\endpoints.py` |
| `endpoints.py` | Other | `backend\app\modules\complaints\endpoints.py` |
| `find_locking_process.ps1` | Other | `backend\find_locking_process.ps1` |
| `fix-all.ps1` | Fix | `scripts\fix-all.ps1` |
| `fix-corrupted-content.py` | Fix | `scripts\fix-corrupted-content.py` |
| `fix-corrupted-filenames.ps1` | Fix | `scripts\fix-corrupted-filenames.ps1` |
| `fix-critical-filenames.py` | Fix | `scripts\scripts\fix-critical-filenames.py` |
| `fix-migration-issues.ps1` | Fix | `scripts\fix-migration-issues.ps1` |
| `fix-sqlalchemy-refs.py` | Fix | `scripts\fix-sqlalchemy-refs.py` |
| `fix-syntax-errors.py` | Fix | `scripts\fix-syntax-errors.py` |
| `fix_and_migrate.ps1` | Fix | `scripts\archived\fix_and_migrate.ps1` |
| `fix_and_migrate.sh` | Fix | `scripts\archived\fix_and_migrate.sh` |
| `fix_linting.py` | Fix | `fix_linting.py` |
| `fix_module_structure.ps1` | Fix | `scripts\fix_module_structure.ps1` |
| `fix_module_structure.py` | Fix | `fix_module_structure.py` |
| `fix_module_structure_fixed.ps1` | Fix | `scripts\fix_module_structure_fixed.ps1` |
| `fix_syntax_errors_targeted.py` | Fix | `scripts\fix_syntax_errors_targeted.py` |
| `fix_unterminated_strings.py` | Fix | `scripts\fix_unterminated_strings.py` |
| `generate-docs.ps1` | Generate | `scripts\generate-docs.ps1` |
| `generate-index.ps1` | Generate | `scripts\generate-index.ps1` |
| `generate-migration-report.py` | Migration | `scripts\generate-migration-report.py` |
| `generate-script-index.ps1` | Generate | `scripts\generate-script-index.ps1` |
| `generate_docs.py` | Generate | `backend\scripts\docs\generate_docs.py` |
| `generate_script_index.py` | Generate | `scripts\generate_script_index.py` |
| `generate_service.py` | Generate | `scripts\generate_service.py` |
| `generate_test_data.py` | Generate | `backend\scripts\generate_test_data.py` |
| `generate_tests.py` | Generate | `scripts\generate_tests.py` |
| `generate_tests_simple.py` | Generate | `scripts\generate_tests_simple.py` |
| `generate_tree.py` | Generate | `generate_tree.py` |
| `init_db.ps1` | Setup | `devops\scripts\init_db.ps1` |
| `init_db.py` | Setup | `backend\init_db.py` |
| `init_db.sh` | Setup | `devops\scripts\init_db.sh` |
| `list_tables.py` | Other | `backend\list_tables.py` |
| `main.py` | Other | `backend\app\main.py` |
| `master-migration.ps1` | Migration | `scripts\master-migration.ps1` |
| `migrate-sqla-to-prisma.ps1` | Migration | `scripts\migrate-sqla-to-prisma.ps1` |
| `migrate_data.py` | Migration | `scripts\migrate_data.py` |
| `migrate_django_to_fastapi.py` | Migration | `scripts\migrate_django_to_fastapi.py` |
| `migrate_django_to_sqlalchemy.py` | Migration | `scripts\migrate_django_to_sqlalchemy.py` |
| `migrate_sqlalchemy_to_prisma.py` | Migration | `backend\scripts\migrate_sqlalchemy_to_prisma.py` |
| `migrate_sqlite_to_postgres.py` | Migration | `scripts\archived\migrate_sqlite_to_postgres.py` |
| `migrate_to_postgres.ps1` | Migration | `migrate_to_postgres.ps1` |
| `migrate_to_postgres.sh` | Migration | `migrate_to_postgres.sh` |
| `migrate_users.py` | Migration | `scripts\migrate_users.py` |
| `models.py` | Other | `backend\app\modules\common\models.py` |
| `models.py` | Other | `backend\app\modules\complaints\models.py` |
| `module_validator.py` | Validator | `scripts\module_validator.py` |
| `move_obsolete_scripts.ps1` | Other | `scripts\move_obsolete_scripts.ps1` |
| `post-migration-audit.ps1` | Migration | `scripts\post-migration-audit.ps1` |
| `prisma-migrate-core.py` | Other | `scripts\prisma-migrate-core.py` |
| `prisma_compatibility_analyzer.py` | Other | `backend\scripts\prisma_compatibility_analyzer.py` |
| `quick_check.py` | Other | `scripts\quick_check.py` |
| `recreate-critical-files.py` | Other | `scripts\recreate-critical-files.py` |
| `recreate_database.py` | Other | `backend\scripts\recreate_database.py` |
| `rollback-prisma-migration.ps1` | Migration | `scripts\rollback-prisma-migration.ps1` |
| `run_all_validations.ps1` | Other | `scripts\run_all_validations.ps1` |
| `run_integration_example.py` | Other | `scripts\run_integration_example.py` |
| `run_prisma_migration.py` | Migration | `backend\scripts\run_prisma_migration.py` |
| `run_tests.ps1` | Test | `backend\scripts\run_tests.ps1` |
| `run_tests.ps1` | Test | `backend\tests\performance\run_tests.ps1` |
| `run_tests.py` | Other | `backend\run_tests.py` |
| `run_tests.sh` | Test | `backend\scripts\run_tests.sh` |
| `run_tests.sh` | Test | `backend\tests\performance\run_tests.sh` |
| `run_tests_with_coverage.ps1` | Test | `backend\scripts\run_tests_with_coverage.ps1` |
| `run_tests_with_coverage.sh` | Test | `backend\scripts\run_tests_with_coverage.sh` |
| `sanear_projeto.ps1` | Other | `sanear_projeto.ps1` |
| `schemas.py` | Other | `backend\app\modules\common\schemas.py` |
| `schemas.py` | Other | `backend\app\modules\complaints\schemas.py` |
| `services.py` | Other | `backend\app\modules\common\services.py` |
| `services.py` | Other | `backend\app\modules\complaints\services.py` |
| `setup.py` | Setup | `backend\app\modules\complaints\setup.py` |
| `setup.py` | Setup | `setup.py` |
| `setup_backend.ps1` | Setup | `backend\setup_backend.ps1` |
| `setup_dev.ps1` | Setup | `backend\scripts\setup_dev.ps1` |
| `setup_env.ps1` | Setup | `scripts\setup_env.ps1` |
| `setup_modules.py` | Setup | `scripts\setup_modules.py` |
| `setup_project_structure.py` | Setup | `scripts\setup_project_structure.py` |
| `setup_structure.py` | Setup | `scripts\setup_structure.py` |
| `sila_migrate.py` | Other | `scripts\sila_migrate.py` |
| `simple_test_data.py` | Other | `backend\scripts\simple_test_data.py` |
| `start.ps1` | Other | `backend\scripts\start.ps1` |
| `sync-endpoints.ps1` | Other | `scripts\sync-endpoints.ps1` |
| `test_api.py` | Test | `backend\test_api.py` |
| `test_appointments.py` | Test | `backend\tests\test_appointments.py` |
| `test_audit.py` | Test | `backend\tests\test_audit.py` |
| `test_auth.py` | Test | `backend\tests\test_auth.py` |
| `test_db_connection.py` | Test | `backend\scripts\test_db_connection.py` |
| `test_directory_structure.py` | Test | `tests\test_directory_structure.py` |
| `test_environment.py` | Test | `scripts\test_environment.py` |
| `test_health.py` | Test | `backend\test_health.py` |
| `test_health.py` | Test | `backend\tests\test_health.py` |
| `test_minimal.py` | Test | `backend\tests\test_minimal.py` |
| `test_password_reset.py` | Test | `backend\tests\test_password_reset.py` |
| `test_permissions.py` | Test | `backend\tests\test_permissions.py` |
| `test_prisma.py` | Test | `backend\test_prisma.py` |
| `test_prisma_connection.py` | Test | `backend\test_prisma_connection.py` |
| `test_prisma_init.py` | Test | `backend\test_prisma_init.py` |
| `test_prisma_minimal.py` | Test | `backend\tests\test_prisma_minimal.py` |
| `test_protocol_flow.py` | Test | `backend\scripts\test_protocol_flow.py` |
| `test_regras_negocio.py` | Test | `backend\tests\test_regras_negocio.py` |
| `test_script.ps1` | Test | `backend\test_script.ps1` |
| `test_sqlite.py` | Test | `backend\scripts\test_sqlite.py` |
| `update_gitignore.ps1` | Other | `scripts\update_gitignore.ps1` |
| `update_models.py` | Other | `update_models.py` |
| `validate-module-integrity.ps1` | Validator | `scripts\validate-module-integrity.ps1` |
| `validate-module-integrity.py` | Validator | `scripts\validate-module-integrity.py` |
| `validate-modules.ps1` | Validator | `scripts\validate-modules.ps1` |
| `validate-py-compile.ps1` | Validator | `scripts\validate-py-compile.ps1` |
| `validate-syntax.py` | Validator | `scripts\validate-syntax.py` |
| `validate_py_compile.py` | Validator | `scripts\validate_py_compile.py` |
| `validate_py_syntax.py` | Validator | `scripts\validate_py_syntax.py` |
| `verify_environment.py` | Other | `backend\verify_environment.py` |
| `verify_module_structure.py` | Other | `verify_module_structure.py` |
| `verify_test_data.py` | Other | `backend\scripts\verify_test_data.py` |
| `wsl_test_db.ps1` | Test | `backend\scripts\wsl_test_db.ps1` |
| `wsl_test_db.sh` | Test | `backend\scripts\wsl_test_db.sh` |


## 🗑️ Diretórios Ignorados

- `.env`
- `.git`
- `.venv`
- `__pycache__`
- `backups`
- `bin`
- `build`
- `dist`
- `env`
- `include`
- `lib`
- `lib64`
- `logs`
- `node_modules`
- `reports`
- `test_venv`
- `venv`

