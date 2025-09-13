"""
Training Mode Module for SILA System

This module provides a complete parallel training environment where users can
safely practice using SILA services without affecting real data.

Key Features:
- Safe sandbox environment with fake data
- Parallel API namespace (/training/)
- Educational tutorials and guidance
- Progress tracking and feedback
- Realistic scenarios for each service
- Multi-language support (PT/EN)

Training Philosophy:
- Learning by doing with realistic scenarios
- Immediate feedback and guidance
- Progressive difficulty levels
- Safe environment for experimentation
- Real-world application focus

Architecture:
- Separate training models and schemas
- Fake data generators using Faker library
- Training-specific routes and services
- Progress tracking and analytics
- Educational content management

Usage:
    from app.modules.training import router as training_router
    app.include_router(training_router)

Access training at: /training/
"""

from fastapi import APIRouter
from app.modules.training.routes.training import router as training_base_router

# Create main training router
router = APIRouter(
    prefix="/training",
    tags=["Training Mode"],
    responses={
        200: {"description": "Training operation successful"},
        400: {"description": "Invalid training request"},
        404: {"description": "Training resource not found"},
        422: {"description": "Training data validation error"}
    }
)

# Include base training routes
router.include_router(training_base_router, tags=["Training System"])

# Training mode middleware to add safety warnings
@router.middleware("http")
async def training_mode_middleware(request, call_next):
    """Add training mode safety headers to all responses"""
    
    response = await call_next(request)
    
    # Add training mode headers
    response.headers["X-Training-Mode"] = "true"
    response.headers["X-Safe-Environment"] = "fake-data-only"
    response.headers["X-Learning-Environment"] = "sila-training"
    
    return response

# Training system health check
@router.get("/", include_in_schema=True)
async def training_system_root():
    """
    Training System Root Endpoint
    
    Welcome endpoint for the SILA training system with safety information.
    """
    
    return {
        "system": "SILA Training Mode",
        "status": "active",
        "version": "1.0.0",
        "warning": "⚠️ TRAINING ENVIRONMENT - All data is fake and safe for learning",
        "description": "Safe learning environment for SILA government services",
        "features": {
            "fake_data_generation": True,
            "safe_operations": True,
            "progress_tracking": True,
            "multi_language": True,
            "realistic_scenarios": True,
            "educational_guidance": True
        },
        "available_endpoints": {
            "status": "/training/status",
            "sessions": "/training/session",
            "modules": "/training/modules", 
            "progress": "/training/progress/{user_name}",
            "fake_data": "/training/fake-data/{type}"
        },
        "learning_modules": [
            {
                "name": "health.consultation",
                "display": "Agendamento de Consulta Médica",
                "path": "/training/health/consultation"
            },
            {
                "name": "citizenship.identity_card", 
                "display": "Solicitação de Carteira de Identidade",
                "path": "/training/citizenship/identity-card"
            },
            {
                "name": "finance.tax_consultation",
                "display": "Consulta de Impostos e Taxas", 
                "path": "/training/finance/tax-consultation"
            },
            {
                "name": "education.enrollment",
                "display": "Matrícula Escolar",
                "path": "/training/education/enrollment"
            },
            {
                "name": "justice.mediation",
                "display": "Solicitação de Mediação",
                "path": "/training/justice/mediation"
            },
            {
                "name": "urbanism.building_permit",
                "display": "Licenciamento de Obras",
                "path": "/training/urbanism/building-permit"
            }
        ],
        "safety_features": [
            "Isolated from production data",
            "Clearly marked fake data",
            "No permanent changes",
            "Educational feedback",
            "Progress tracking",
            "Safe experimentation"
        ],
        "getting_started": {
            "step_1": "Choose a learning module from the list above",
            "step_2": "Create a training session with your name",
            "step_3": "Follow the interactive tutorial",
            "step_4": "Practice with different scenarios", 
            "step_5": "Complete exercises and get feedback"
        }
    }

__all__ = ["router"]