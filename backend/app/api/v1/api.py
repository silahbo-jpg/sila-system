"""
API v1 Router Configuration.

This module aggregates all API v1 routes and includes them under the /api/v1 prefix.
"""
from fastapi import APIRouter

# Import all route modules
from app.modules.citizenship.routes.emissao_bi_route import router as emissao_bi_router
from app.api.v1.endpoints import auth, users

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include all route modules
api_router.include_router(
    emissao_bi_router,
    prefix="/citizenship",
    tags=["Citizenship"]
)

# Include auth and users routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Health check endpoint
@api_router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Root endpoint
@api_router.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SILA System API",
        "version": "1.0.0",
        "docs": "/api/v1/docs"
    }
