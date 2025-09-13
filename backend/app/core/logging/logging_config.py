# backend/app/core/logging_config.py
"""
Configuração centralizada de logging para o projeto SILA.
Versão simplificada e funcional para saneamento do projeto.
"""

import logging
import logging.config
import sys
import json
from pathlib import Path
from datetime import datetime

# Caminhos para os diretórios de log
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "sila.log"
ERROR_LOG_FILE = LOG_DIR / "sila_error.log"

# Garante que o diretório de logs existe
LOG_DIR.mkdir(exist_ok=True, parents=True)

# Variável global `logger` — necessária para evitar ImportError
logger = logging.getLogger("postgres-api")

class JsonFormatter(logging.Formatter):
    """Formata as mensagens de log como JSON estruturado."""
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Adiciona campos extras
        if hasattr(record, "args") and isinstance(record.args, dict):
            log_record.update(record.args)

        return json.dumps(log_record, ensure_ascii=False, default=str)

def setup_logging(
    log_level: int = logging.INFO,
    use_emojis: bool = False,
    json_format: bool = True,
    log_to_file: bool = True,
    log_to_console: bool = True) -> None:
    """Configura o sistema de logging."""
    # Remove handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Define nível global
    logger.setLevel(log_level)

    formatter = JsonFormatter() if json_format else logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.stream.reconfigure(encoding='utf-8')  # Ensure UTF-8 encoding
        
        if use_emojis:
            console_handler.setFormatter(JsonFormatter())
        else:
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
        
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

    if log_to_file:
        # Handler para logs gerais
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler para erros
        error_handler = logging.FileHandler(ERROR_LOG_FILE)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

    # Configuração de bibliotecas externas
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# ⚠️ Não chamar setup_logging() aqui → será chamado explicitamente em main.py

