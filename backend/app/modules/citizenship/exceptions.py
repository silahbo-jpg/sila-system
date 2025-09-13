"""
Custom exceptions for the citizenship module.

This module defines all custom exceptions used throughout the citizenship module.
"""

from fastapi import status
from fastapi.exceptions import HTTPException
from typing import Any, Dict, Optional, Union


class CitizenshipError(Exception):
    """Base exception for all citizenship-related errors."""
    def __init__(self, message: str, code: str = "citizenship_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class CitizenNotFoundError(CitizenshipError):
    """Raised when a citizen is not found."""
    def __init__(self, citizen_id: Optional[Union[int, str]] = None):
        message = f"Citizen not found"
        if citizen_id is not None:
            message += f" with ID: {citizen_id}"
        super().__init__(message, "citizen_not_found")


class DocumentNotFoundError(CitizenshipError):
    """Raised when a document is not found."""
    def __init__(self, document_id: Optional[Union[int, str]] = None):
        message = "Document not found"
        if document_id is not None:
            message += f" with ID: {document_id}"
        super().__init__(message, "document_not_found")


class DuplicateCitizenError(CitizenshipError):
    """Raised when trying to create a citizen that already exists."""
    def __init__(self, identifier: str, identifier_type: str = "NIF"):
        super().__init__(
            f"Citizen with {identifier_type} '{identifier}' already exists",
            "duplicate_citizen"
        )


class InvalidDocumentError(CitizenshipError):
    """Raised when a document is invalid."""
    def __init__(self, details: str):
        super().__init__(f"Invalid document: {details}", "invalid_document")


class DocumentVerificationError(CitizenshipError):
    """Raised when document verification fails."""
    def __init__(self, details: str):
        super().__init__(f"Document verification failed: {details}", "document_verification_failed")


class AddressValidationError(CitizenshipError):
    """Raised when address validation fails."""
    def __init__(self, details: str):
        super().__init__(f"Address validation failed: {details}", "address_validation_failed")


def handle_citizenship_error(error: CitizenshipError) -> HTTPException:
    """Convert a CitizenshipError to an HTTPException.
    
    Args:
        error: The CitizenshipError to convert.
        
    Returns:
        HTTPException: The corresponding HTTP exception.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    
    if isinstance(error, (CitizenNotFoundError, DocumentNotFoundError)):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(error, (InvalidDocumentError, DocumentVerificationError, AddressValidationError)):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(error, DuplicateCitizenError):
        status_code = status.HTTP_409_CONFLICT
    
    return HTTPException(
        status_code=status_code,
        detail={
            "code": error.code,
            "message": str(error),
            "type": error.__class__.__name__
        }
    )
