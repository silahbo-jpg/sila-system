"""
Core Location Module

This module handles the hierarchical location structure:
Country → Province → Municipality → Commune

Provides services for location management and address validation.
"""

from .services import LocationService
from .models import (
    CountryCreate, CountryUpdate, CountryResponse,
    ProvinceCreate, ProvinceUpdate, ProvinceResponse,
    MunicipalityCreate, MunicipalityUpdate, MunicipalityResponse,
    CommuneCreate, CommuneUpdate, CommuneResponse,
    FullAddressResponse, LocationHierarchy
)
from .schemas import *

__all__ = [
    "LocationService",
    "CountryCreate", "CountryUpdate", "CountryResponse",
    "ProvinceCreate", "ProvinceUpdate", "ProvinceResponse",
    "MunicipalityCreate", "MunicipalityUpdate", "MunicipalityResponse",
    "CommuneCreate", "CommuneUpdate", "CommuneResponse",
    "FullAddressResponse", "LocationHierarchy"
]