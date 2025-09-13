"""
API Versioning Infrastructure for SILA System

This module provides versioning capabilities for all API endpoints,
allowing multiple API versions to coexist and automatic latest version routing.
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, Request, HTTPException
from fastapi.routing import APIRoute
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class APIVersion(str, Enum):
    """Supported API versions"""
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"
    LATEST = "latest"

class VersionManager:
    """Manages API version routing and compatibility"""
    
    def __init__(self):
        self.versions: Dict[str, APIRouter] = {}
        self.latest_version = APIVersion.V1
        self.version_compatibility: Dict[str, List[str]] = {}
        
    def register_version(self, version: APIVersion, router: APIRouter):
        """Register a versioned API router"""
        self.versions[version.value] = router
        logger.info(f"Registered API version: {version.value}")
        
    def set_latest_version(self, version: APIVersion):
        """Set which version is considered 'latest'"""
        if version.value in self.versions:
            self.latest_version = version
            logger.info(f"Latest API version set to: {version.value}")
        else:
            raise ValueError(f"Version {version.value} not registered")
            
    def get_version_router(self, version: str) -> APIRouter:
        """Get router for specific version"""
        if version == APIVersion.LATEST.value:
            version = self.latest_version.value
            
        if version not in self.versions:
            raise HTTPException(
                status_code=404, 
                detail=f"API version {version} not found. Available versions: {list(self.versions.keys())}"
            )
            
        return self.versions[version]
        
    def get_available_versions(self) -> List[str]:
        """Get list of all available API versions"""
        return list(self.versions.keys()) + [APIVersion.LATEST.value]
        
    def add_compatibility(self, from_version: str, to_versions: List[str]):
        """Add version compatibility mapping for migration support"""
        self.version_compatibility[from_version] = to_versions

# Global version manager instance
version_manager = VersionManager()

def create_versioned_router(
    version: APIVersion,
    title: str = None,
    description: str = None,
    tags: List[str] = None
) -> APIRouter:
    """
    Create a versioned API router with automatic registration
    
    Args:
        version: API version enum
        title: Optional router title
        description: Optional router description  
        tags: Optional list of tags for OpenAPI
        
    Returns:
        Configured APIRouter for the specified version
    """
    router = APIRouter(
        tags=tags or [f"API {version.value.upper()}"],
        responses={
            404: {"description": "Not found"},
            422: {"description": "Validation Error"},
            500: {"description": "Internal Server Error"}
        }
    )
    
    # Add version info endpoint
    @router.get("/version", tags=["Version Info"])
    async def get_version_info():
        """Get information about this API version"""
        return {
            "version": version.value,
            "title": title or f"SILA API {version.value}",
            "description": description or f"SILA System API version {version.value}",
            "is_latest": version.value == version_manager.latest_version.value,
            "available_versions": version_manager.get_available_versions()
        }
    
    # Register with version manager
    version_manager.register_version(version, router)
    
    return router

def version_route(version: APIVersion):
    """Decorator to mark routes as version-specific"""
    def decorator(func):
        func._api_version = version.value
        return func
    return decorator

async def version_middleware(request: Request, call_next):
    """Middleware to handle version-specific requests and compatibility"""
    response = await call_next(request)
    
    # Add version headers
    if hasattr(request.state, 'api_version'):
        response.headers["X-API-Version"] = request.state.api_version
        response.headers["X-API-Latest"] = version_manager.latest_version.value
        
    return response

def get_version_from_path(path: str) -> Optional[str]:
    """Extract version from request path"""
    path_parts = path.strip('/').split('/')
    if len(path_parts) >= 2 and path_parts[0] == 'api':
        version_part = path_parts[1]
        if version_part in [v.value for v in APIVersion]:
            return version_part
    return None

# Version deprecation warnings
VERSION_DEPRECATION_WARNINGS = {
    APIVersion.V1: {
        "deprecated": False,
        "sunset_date": None,
        "migration_guide": None
    }
}

def add_deprecation_warning(
    version: APIVersion, 
    sunset_date: str = None, 
    migration_guide: str = None
):
    """Add deprecation warning for a specific version"""
    VERSION_DEPRECATION_WARNINGS[version] = {
        "deprecated": True,
        "sunset_date": sunset_date,
        "migration_guide": migration_guide
    }
    logger.warning(f"API version {version.value} marked as deprecated")