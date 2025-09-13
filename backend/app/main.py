"""
Main FastAPI application entrypoint.

This module initializes logging, observability, and runs the application.
"""

import logging

from app.core.logging.logging_config import logger, setup_logging
from observability.sentry_config import init_sentry
from app.core.application import app
from app.core.config import settings

# Configure logging without emojis for Windows compatibility
setup_logging(use_emojis=False, log_level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger.info("Application started", extra={"version": settings.VERSION})

# Initialize observability
init_sentry()

# Allow running with `uvicorn app.main:app`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
        workers=settings.WORKERS)
