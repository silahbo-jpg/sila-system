"""
Test-specific logging configuration that disables structured logging and ensures clean test output.
"""
import logging
import sys
import json
from typing import Any, Dict, Optional

class PlainTextFormatter(logging.Formatter):
    """A simple formatter that outputs plain text logs without JSON formatting."""
    
    def format(self, record: logging.LogRecord) -> str:
        # If the message is a dict (from structured logging), convert it to a string
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg, indent=2, ensure_ascii=False)
        return super().format(record)

def configure_test_logging() -> None:
    """Configure logging for tests to ensure clean output."""
    # Remove all existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure console handler with plain text formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        PlainTextFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    )
    
    # Set up the root logger
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    # Disable specific loggers that are too verbose during testing
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    # Disable specific application loggers that might interfere
    logging.getLogger('postgres-api').setLevel(logging.WARNING)

# Apply the configuration when this module is imported
configure_test_logging()
