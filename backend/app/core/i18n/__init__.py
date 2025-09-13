"""
i18n Module Initialization

This module provides internationalization (i18n) support for the SILA system.
"""

from pathlib import Path
from typing import Optional
from fastapi import Request

from .i18n import (
    TranslationManager,
    initialize_translations,
    i18n_middleware,
    get_current_language,
    translate,
    t as _
)

__all__ = [
    'TranslationManager',
    'initialize_translations',
    'i18n_middleware',
    'get_current_language',
    'translate',
    '_'  # Short alias for translate
]