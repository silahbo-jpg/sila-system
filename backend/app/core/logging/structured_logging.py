# backend/app/core/structured_logging.py
"""
Logging estruturado simplificado para o projeto SILA.
Substitui structlog por logging padrão para evitar dependências não instaladas.
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Diretório de logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configuração do formato JSON
class JsonFormatter:
    """Formatador simples para logs em JSON."""
    @staticmethod
    def format(record: logging.LogRecord, extra: Dict[str, Any] = None) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_entry["exception"] = str(record.exc_info[1])
        if extra:
            log_entry.update(extra)
        return json.dumps(log_entry, ensure_ascii=False, default=str)

# Logger global
logger = logging.getLogger("postgres-api")

def setup_structured_logging() -> None:
    """Configuração básica de logging em JSON."""
    # Evita múltiplos handlers
    if logger.handlers:
        return

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))  # O JSON será a mensagem
    logger.addHandler(handler)

    # Exemplo de log de inicialização
    logger.info(JsonFormatter.format(
        logging.LogRecord(
            name=logger.name,
            level=logging.INFO,
            pathname=__file__,
            lineno=60,
            msg="Structured logging configured",
            args=(),
            exc_info=None
        ),
        extra={
            "environment": "development",
            "service": "postgres-api",
            "version": "0.1.0",
            "log_level": "INFO"
        }
    ))

def get_structured_logger(name: Optional[str] = None) -> logging.Logger:
    """Retorna o logger configurado."""
    return logger

# Inicializa ao importar
setup_structured_logging()

# Exporta para compatibilidade
logger = get_structured_logger(__name__)

