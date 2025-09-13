# Database Initialization

## Script
- `ensure_databases.sql`: Verifica e cria os bancos `sila_dev` e `sila_test` se não existirem.

## Execução
```powershell
psql -U postgres -h localhost -p 5432 -f "ensure_databases.sql" > db_creation.log 2>&1

