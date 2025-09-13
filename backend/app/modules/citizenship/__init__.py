"""
Módulo de Cidadania do SILA.

Este módulo fornece funcionalidades para gerenciar cidadãos, documentos e feedbacks,
além de validações e regras de negócio relacionadas à cidadania.
"""
from typing import Any, Dict, List, Optional, Type, Union

from fastapi import FastAPI, HTTPException, Request, status

# Core exports
__all__ = [
    # Exception classes
    "CitizenshipError",
    "CitizenNotFoundError",
    "DocumentNotFoundError",
    "DuplicateCitizenError",
    "InvalidDocumentError",
    "DocumentVerificationError",
    "AddressValidationError",
    
    # Handler functions
    "citizenship_exception_handler",
    "register_exception_handlers",
    "setup_error_handling",
    "setup_citizenship_module",
    "ERROR_RESPONSES"
]

# Lazy imports to avoid circular dependencies
def __getattr__(name: str) -> Any:
    if name == "exceptions":
        from . import exceptions as _exceptions
        return _exceptions
    if name == "handlers":
        from . import handlers as _handlers
        return _handlers
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# Import exceptions
from .exceptions import (
    CitizenshipError,
    CitizenNotFoundError,
    DocumentNotFoundError,
    DuplicateCitizenError,
    InvalidDocumentError,
    DocumentVerificationError,
    AddressValidationError,
)

# Import handlers
from .handlers import (
    citizenship_exception_handler,
    register_exception_handlers,
    setup_error_handling,
    ERROR_RESPONSES
)

def setup_citizenship_module(app: FastAPI) -> None:
    """
    Configura o módulo de cidadania na aplicação FastAPI.
    
    Args:
        app: Instância da aplicação FastAPI
    """
    # Configure error handling
    setup_error_handling(app)
    
    # Import router here to avoid circular imports
    from .routes import router as citizenship_router
    
    # Include the router
    app.include_router(
        citizenship_router,
        prefix="/api/v1/citizenship",
        tags=["citizenship"]
    )
    
    # Log setup completion
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Módulo de Cidadania configurado com sucesso")
