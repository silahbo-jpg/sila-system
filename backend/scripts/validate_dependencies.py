# -*- coding: utf-8 -*-
import importlib
import sys

# Ensure stdout uses UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

MODULES_TO_VALIDATE = {
    "fastapi": "FastAPI framework",
    "starlette": "ASGI toolkit",
    "pydantic": "Data validation",
    "sqlalchemy": "ORM",
    "asyncpg": "Async PostgreSQL driver",
    "sentry_sdk": "Error tracking",
    "structlog": "Structured logging",
    "opentelemetry.trace": "OpenTelemetry Tracing API",
    "opentelemetry.sdk": "OpenTelemetry SDK",
    "opentelemetry.exporter.otlp": "OTLP Exporter",
    "opentelemetry.exporter.jaeger": "Jaeger Exporter",
    "opentelemetry.instrumentation.fastapi": "FastAPI Instrumentation",
    "opentelemetry.instrumentation.sqlalchemy": "SQLAlchemy Instrumentation",
    "deprecated": "Deprecation decorator",
}

def validate_module(module_path, description):
    try:
        module = importlib.import_module(module_path)
        version = getattr(module, "__version__", "✅ instalado (versão não disponível)")
        print(f"✅ {description}: {module_path} — versão: {version}")
    except ImportError as e:
        print(f"❌ {description}: {module_path} — erro: {e}")

if __name__ == "__main__":
    print("🔍 Validando módulos críticos do projeto...\n")
    for path, label in MODULES_TO_VALIDATE.items():
        validate_module(path, label)
