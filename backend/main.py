"""
Compatibility entrypoint for FastAPI.

This file exists only to allow running the app with:
    uvicorn main:app --reload
but delegates the real application to `app/main.py`.
"""

from app.main import app  # Import the actual FastAPI app

if __name__ == "__main__":
    import uvicorn
    from app.core.config import get_settings
    
    settings = get_settings()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
        workers=1 if settings.DEBUG else settings.WORKERS,
    )
