from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.db.session import init_db

logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This function initializes the application with all necessary middleware,
    routes, and database connections using Prisma ORM.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json"
    )

    # =========================
    # Middleware Configuration
    # =========================
    from app.core.i18n import i18n_middleware, initialize_translations
    from pathlib import Path
    
    # Initialize translation system
    translations_dir = Path(__file__).parent.parent.parent.parent / "translations"
    translations_dir.mkdir(exist_ok=True)
    initialize_translations(translations_dir)
    
    # Add i18n middleware
    app.middleware("http")(i18n_middleware)
    
    # CORS Middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"])

    # =========================
    # API Routers with Versioning
    # =========================
    from app.api.v1.api import api_router
    app.include_router(api_router)
    
    # Initialize database on startup
    @app.on_event("startup")
    async def startup_event():
        await init_db()

    # Add health check endpoints
    @app.get("/ping")
    def ping():
        """Simple health check endpoint"""
        return {"status": "ok", "message": "SILA API is running"}
    
    @app.get("/health")
    def health():
        """Health check endpoint with service status"""
        return {
            "status": "healthy", 
            "service": "sila-api",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        }

    return app


# Global instance used by ASGI servers and tests
app = create_application()
