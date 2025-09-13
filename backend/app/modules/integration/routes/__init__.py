from fastapi import APIRouter
from app.modules.integration.routes.event_routes import router as event_router

router = APIRouter()
router.include_router(event_router, prefix="/events", tags=["integration"])

__all__ = ["router"]

