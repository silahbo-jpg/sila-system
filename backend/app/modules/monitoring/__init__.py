"""
Monitoring Module

This module provides comprehensive observability for the SILA system including:
- OpenTelemetry integration for distributed tracing
- Prometheus metrics collection
- Grafana dashboard configurations
- Health check endpoints
- Performance monitoring
"""

from fastapi import APIRouter
from app.modules.monitoring.routes.metrics import router as metrics_router
from app.modules.monitoring.routes.health import router as health_router
from app.modules.monitoring.routes.tracing import router as tracing_router

# Create monitoring router
router = APIRouter(prefix="/monitoring", tags=["Monitoring & Observability"])

# Include all monitoring routes
router.include_router(metrics_router)
router.include_router(health_router)
router.include_router(tracing_router)

__all__ = ["router"]