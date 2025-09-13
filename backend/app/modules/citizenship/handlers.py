"""
Exception handlers for the citizenship module.

This module contains exception handlers for the citizenship module,
converting domain exceptions to appropriate HTTP responses.
"""

from typing import Callable, Type, Dict, Any, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse

from . import exceptions as citizenship_exceptions


async def citizenship_exception_handler(
    request: Request, 
    exc: citizenship_exceptions.CitizenshipError
) -> JSONResponse:
    """Handle CitizenshipError exceptions.
    
    Args:
        request: The request that caused the exception.
        exc: The exception that was raised.
        
    Returns:
        JSONResponse: The error response.
    """
    return citizenship_exceptions.handle_citizenship_error(exc)


def register_exception_handlers(app):
    """Register exception handlers for the citizenship module.
    
    Args:
        app: The FastAPI application instance.
    """
    app.add_exception_handler(
        citizenship_exceptions.CitizenshipError,
        citizenship_exception_handler
    )
    
    # Register specific exception handlers if needed
    for exc_type in [
        citizenship_exceptions.CitizenNotFoundError,
        citizenship_exceptions.DocumentNotFoundError,
        citizenship_exceptions.DuplicateCitizenError,
        citizenship_exceptions.InvalidDocumentError,
        citizenship_exceptions.DocumentVerificationError,
        citizenship_exceptions.AddressValidationError,
    ]:
        app.add_exception_handler(
            exc_type,
            citizenship_exception_handler
        )


def setup_error_handling(app):
    """Set up error handling for the citizenship module.
    
    This function should be called during application startup.
    
    Args:
        app: The FastAPI application instance.
    """
    register_exception_handlers(app)


# Common error responses for OpenAPI documentation
ERROR_RESPONSES: Dict[int, Dict[str, Any]] = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "validation_error",
                        "message": "Invalid input data",
                        "type": "ValidationError"
                    }
                }
            }
        }
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated"
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not enough permissions"
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "citizen_not_found",
                        "message": "Citizen not found with ID: 123",
                        "type": "CitizenNotFoundError"
                    }
                }
            }
        }
    },
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "duplicate_citizen",
                        "message": "Citizen with NIF '123456789' already exists",
                        "type": "DuplicateCitizenError"
                    }
                }
            }
        }
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "nif"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "An unexpected error occurred"
                }
            }
        }
    }
}
