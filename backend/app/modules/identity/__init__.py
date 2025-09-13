"""
Core Identity Module

This module handles citizen identity management with validated addresses.
Every citizen profile includes the complete address hierarchy:
Country → Province → Municipality → Commune → Neighborhood → Street → House

Key features:
- Validated address storage
- Reusable citizen profiles across all services
- BI (Bilhete de Identidade) validation
- Profile verification system
"""

from .services import CitizenService
from .models import (
    CitizenCreate, CitizenUpdate, CitizenResponse,
    CitizenRegistration, CitizenVerification,
    CitizenSearchFilters
)
from .schemas import *

__all__ = [
    "CitizenService",
    "CitizenCreate", "CitizenUpdate", "CitizenResponse",
    "CitizenRegistration", "CitizenVerification",
    "CitizenSearchFilters"
]