"""
Training Mode Module for SILA System

This module provides a parallel training environment where users can practice
using SILA services without affecting real data. It includes:
- Parallel API namespace (/training/)
- Fake data generation using Faker library
- Selected service replicas for training
- Safe environment indicators
- Training session management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.db.session import get_db
from app.modules.training.models import TrainingSession, TrainingModule, TrainingUser
from app.modules.training.schemas import (
    TrainingSessionCreate, TrainingSessionRead, 
    TrainingModuleCreate, TrainingModuleRead,
    TrainingUserCreate, TrainingUserRead
)
from app.modules.training.fake_data import FakeDataGenerator
import logging

logger = logging.getLogger(__name__)

# Create training router with special prefix
router = APIRouter(prefix="/training", tags=["Training Mode"])

@router.get("/status")
async def training_mode_status():
    """
    Get training mode system status
    
    Returns information about available training modules and system health.
    """
    
    return {
        "status": "active",
        "mode": "training",
        "warning": "⚠️ TRAINING MODE - No real data will be modified",
        "description": "Safe environment for learning and testing SILA services",
        "available_modules": [
            "health.consultation",
            "citizenship.identity_card", 
            "finance.tax_consultation",
            "education.enrollment",
            "justice.mediation",
            "urbanism.building_permit"
        ],
        "features": {
            "fake_data": True,
            "safe_operations": True,
            "real_time_feedback": True,
            "progress_tracking": True
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/session", response_model=TrainingSessionRead)
async def create_training_session(
    data: TrainingSessionCreate):
    """
    Create a new training session
    
    Training sessions allow users to practice in a controlled environment
    with fake data and guided workflows.
    """
    
    # Generate fake user data for this training session
    fake_generator = FakeDataGenerator()
    fake_citizen = fake_generator.generate_citizen_data()
    
    # Create training session
    session = TrainingSession(
        user_name=data.user_name,
        training_module=data.training_module,
        session_type=data.session_type,
        difficulty_level=data.difficulty_level,
        fake_citizen_data=fake_citizen,
        status="active",
        start_time=datetime.utcnow()
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    logger.info(f"Training session created: {session.id} for module {data.training_module}")
    
    return session

@router.get("/session/{session_id}", response_model=TrainingSessionRead)
async def get_training_session(session_id: int):
    """Get details of a specific training session"""
    
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")
        
    return session

@router.get("/sessions", response_model=List[TrainingSessionRead])
async def list_training_sessions(
    user_name: Optional[str] = Query(None),
    module: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100)):
    """List training sessions with optional filters"""
    
    query = db.query(TrainingSession)
    
    if user_name:
        query = query.filter(TrainingSession.user_name == user_name)
    if module:
        query = query.filter(TrainingSession.training_module == module)
    if status:
        query = query.filter(TrainingSession.status == status)
        
    sessions = query.order_by(TrainingSession.start_time.desc()).limit(limit).all()
    return sessions

@router.put("/session/{session_id}/complete")
async def complete_training_session(
    session_id: int,
    score: int = Query(ge=0, le=100),
    feedback: Optional[str] = Query(None)):
    """Mark a training session as completed with score and feedback"""
    
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")
        
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Session already completed")
    
    # Update session
    session.status = "completed"
    session.end_time = datetime.utcnow()
    session.completion_score = score
    session.feedback = feedback
    
    # Calculate duration
    if session.start_time:
        duration = session.end_time - session.start_time
        session.duration_minutes = int(duration.total_seconds() / 60)
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Training session completed successfully",
        "session_id": session_id,
        "score": score,
        "duration_minutes": session.duration_minutes
    }

@router.get("/modules", response_model=List[TrainingModuleRead])
async def list_training_modules():
    """Get list of available training modules"""
    
    modules = db.query(TrainingModule).filter(TrainingModule.is_active == True).all()
    
    # If no modules in database, return predefined modules
    if not modules:
        predefined_modules = [
            {
                "id": 1,
                "module_name": "health.consultation",
                "display_name": "Agendamento de Consulta Médica",
                "description": "Aprenda a agendar consultas médicas no sistema de saúde",
                "difficulty_level": "beginner",
                "estimated_duration": 15,
                "learning_objectives": [
                    "Navegar no módulo de saúde",
                    "Preencher formulário de agendamento",
                    "Confirmar consulta médica"
                ],
                "is_active": True
            },
            {
                "id": 2,
                "module_name": "citizenship.identity_card", 
                "display_name": "Solicitação de Carteira de Identidade",
                "description": "Pratique o processo de solicitação de documentos de identidade",
                "difficulty_level": "intermediate",
                "estimated_duration": 25,
                "learning_objectives": [
                    "Compreender requisitos documentais",
                    "Preencher formulário de solicitação",
                    "Acompanhar status do pedido"
                ],
                "is_active": True
            },
            {
                "id": 3,
                "module_name": "justice.mediation",
                "display_name": "Solicitação de Mediação",
                "description": "Aprenda a solicitar serviços de mediação de conflitos",
                "difficulty_level": "advanced",
                "estimated_duration": 30,
                "learning_objectives": [
                    "Identificar casos para mediação",
                    "Preencher formulário detalhado",
                    "Entender processo de mediação"
                ],
                "is_active": True
            }
        ]
        return predefined_modules
        
    return modules

@router.post("/module", response_model=TrainingModuleRead)
async def create_training_module(
    data: TrainingModuleCreate):
    """Create a new training module"""
    
    # Check if module already exists
    existing = db.query(TrainingModule).filter(
        TrainingModule.module_name == data.module_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Training module already exists"
        )
    
    module = TrainingModule(**data.dict())
    db.add(module)
    db.commit()
    db.refresh(module)
    
    logger.info(f"Training module created: {module.module_name}")
    
    return module

@router.get("/fake-data/citizen")
async def generate_fake_citizen():
    """Generate fake citizen data for training purposes"""
    
    fake_generator = FakeDataGenerator()
    citizen_data = fake_generator.generate_citizen_data()
    
    return {
        "status": "success",
        "warning": "🤖 This is fake data for training purposes only",
        "data": citizen_data
    }

@router.get("/fake-data/{data_type}")
async def generate_fake_data_by_type(data_type: str):
    """Generate specific types of fake data"""
    
    fake_generator = FakeDataGenerator()
    
    data_generators = {
        "appointment": fake_generator.generate_appointment_data,
        "document": fake_generator.generate_document_data,
        "address": fake_generator.generate_address_data,
        "contact": fake_generator.generate_contact_data,
        "business": fake_generator.generate_business_data,
        "financial": fake_generator.generate_financial_data
    }
    
    if data_type not in data_generators:
        raise HTTPException(
            status_code=400,
            detail=f"Data type '{data_type}' not supported. Available: {list(data_generators.keys())}"
        )
    
    data = data_generators[data_type]()
    
    return {
        "status": "success",
        "type": data_type,
        "warning": "🤖 This is fake data for training purposes only",
        "data": data
    }

@router.get("/progress/{user_name}")
async def get_training_progress(user_name: str):
    """Get training progress for a specific user"""
    
    # Get user's completed sessions
    completed_sessions = db.query(TrainingSession).filter(
        TrainingSession.user_name == user_name,
        TrainingSession.status == "completed"
    ).all()
    
    # Calculate progress statistics
    total_sessions = len(completed_sessions)
    avg_score = sum(s.completion_score or 0 for s in completed_sessions) / max(total_sessions, 1)
    total_time = sum(s.duration_minutes or 0 for s in completed_sessions)
    
    # Group by module
    modules_progress = {}
    for session in completed_sessions:
        module = session.training_module
        if module not in modules_progress:
            modules_progress[module] = {
                "sessions_completed": 0,
                "average_score": 0,
                "total_time_minutes": 0,
                "best_score": 0
            }
        
        modules_progress[module]["sessions_completed"] += 1
        modules_progress[module]["total_time_minutes"] += session.duration_minutes or 0
        modules_progress[module]["best_score"] = max(
            modules_progress[module]["best_score"],
            session.completion_score or 0
        )
    
    # Calculate average scores per module
    for module_data in modules_progress.values():
        module_sessions = [s for s in completed_sessions if s.training_module == module]
        if module_sessions:
            module_data["average_score"] = sum(
                s.completion_score or 0 for s in module_sessions
            ) / len(module_sessions)
    
    return {
        "user_name": user_name,
        "overall_progress": {
            "total_sessions_completed": total_sessions,
            "average_score": round(avg_score, 1),
            "total_training_time_minutes": total_time,
            "skill_level": _calculate_skill_level(avg_score, total_sessions)
        },
        "modules_progress": modules_progress,
        "achievements": _calculate_achievements(completed_sessions),
        "recommendations": _get_recommendations(modules_progress)
    }

def _calculate_skill_level(avg_score: float, total_sessions: int) -> str:
    """Calculate user skill level based on performance"""
    
    if total_sessions == 0:
        return "beginner"
    elif total_sessions < 5:
        return "novice"
    elif avg_score >= 90 and total_sessions >= 10:
        return "expert"
    elif avg_score >= 75 and total_sessions >= 5:
        return "advanced"
    elif avg_score >= 60:
        return "intermediate"
    else:
        return "beginner"

def _calculate_achievements(sessions: List[TrainingSession]) -> List[Dict]:
    """Calculate user achievements based on training history"""
    
    achievements = []
    
    # First completion
    if sessions:
        achievements.append({
            "name": "First Steps",
            "description": "Completed your first training session",
            "earned_date": min(s.end_time for s in sessions if s.end_time).isoformat()
        })
    
    # High scorer
    high_scores = [s for s in sessions if (s.completion_score or 0) >= 90]
    if len(high_scores) >= 3:
        achievements.append({
            "name": "High Achiever",
            "description": "Scored 90% or higher in 3+ sessions",
            "earned_date": high_scores[2].end_time.isoformat()
        })
    
    # Module explorer
    unique_modules = set(s.training_module for s in sessions)
    if len(unique_modules) >= 3:
        achievements.append({
            "name": "Module Explorer",
            "description": "Completed training in 3 different modules",
            "earned_date": datetime.utcnow().isoformat()
        })
    
    return achievements

def _get_recommendations(modules_progress: Dict) -> List[str]:
    """Get personalized training recommendations"""
    
    recommendations = []
    
    if not modules_progress:
        recommendations.append("Start with health.consultation module - it's great for beginners!")
        recommendations.append("Try the citizenship.identity_card module to learn document processes")
        return recommendations
    
    # Find weakest module
    weakest_module = min(
        modules_progress.items(), 
        key=lambda x: x[1]["average_score"]
    )
    
    if weakest_module[1]["average_score"] < 75:
        recommendations.append(f"Practice more with {weakest_module[0]} - your average score is {weakest_module[1]['average_score']:.1f}%")
    
    # Suggest new modules
    completed_modules = set(modules_progress.keys())
    all_modules = {
        "health.consultation", "citizenship.identity_card", "finance.tax_consultation",
        "education.enrollment", "justice.mediation", "urbanism.building_permit"
    }
    
    remaining_modules = all_modules - completed_modules
    if remaining_modules:
        next_module = list(remaining_modules)[0]
        recommendations.append(f"Try the {next_module} module to expand your skills")
    
    return recommendations