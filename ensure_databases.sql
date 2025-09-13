-- ensure_databases.sql
-- Verifica e cria os bancos sila_dev e sila_test se não existirem

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sila_dev') THEN
    CREATE DATABASE sila_dev
      WITH OWNER = postgres
      ENCODING = 'UTF8'
      LC_COLLATE = 'Portuguese_Portugal.1252'
      LC_CTYPE = 'Portuguese_Portugal.1252'
      TEMPLATE = template0;
  END IF;

  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sila_test') THEN
    CREATE DATABASE sila_test
      WITH OWNER = postgres
      ENCODING = 'UTF8'
      LC_COLLATE = 'Portuguese_Portugal.1252'
      LC_CTYPE = 'Portuguese_Portugal.1252'
      TEMPLATE = template0;
  END IF;
END $$;

