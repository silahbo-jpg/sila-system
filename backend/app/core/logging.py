"""
Logging configuration for the SILA application.

This module sets up logging with appropriate formatting and handlers.
"""
import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, Any

from app.core.config import settings

def setup_logging() -> None:
    """
    Configure logging for the application.
    
    Sets up console and file logging with appropriate formatting.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(funcName)s %(lineno)d"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "standard",
                "filename": log_dir / "sila.log",
                "maxBytes": 10 * 1024 * 1024,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": "DEBUG" if settings.ENVIRONMENT == "development" else "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "postgres": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    }
    
    logging.config.dictConfig(log_config)
    logging.captureWarnings(True)

