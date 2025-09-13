"""
Core functionality for the SILA application.

This module contains core components like configuration, database connections,
logging setup, and other fundamental services used throughout the application.
"""

from .config import Settings, get_settings, settings
from .logging.structured_logging import (
    get_structured_logger,
    setup_structured_logging,
    logger)

# Initialize logging when the module is imported
setup_structured_logging()

__all__ = [
    # Configuration
    'Settings',
    'get_settings',
    'settings',
    
    # Logging
    'get_structured_logger',
    'setup_structured_logging',
    'logger',
]

