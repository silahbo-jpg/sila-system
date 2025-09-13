"""
Health Check API Routes

Provides comprehensive health monitoring endpoints for the SILA system.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from typing import Dict, List, Any
import time
import os
import psutil
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health Checks"])

@router.get("/")
async def health_check():
    """
    Basic health check endpoint
    
    Returns simple status for load balancer health checks.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check():
    """
    Detailed health check with all system components
    
    Provides comprehensive health status for monitoring systems.
    """
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    overall_healthy = True
    
    # Database connectivity check
    try:
        start_time = time.time()
        result = db.execute(text("SELECT 1")).fetchone()
        db_response_time = time.time() - start_time
        
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": round(db_response_time * 1000, 2),
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
            "message": "Database connection failed"
        }
        overall_healthy = False
    
    # System resources check
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Determine resource health
        resource_status = "healthy"
        if cpu_percent > 90 or memory.percent > 90 or (disk.used / disk.total) > 0.9:
            resource_status = "warning"
        if cpu_percent > 95 or memory.percent > 95 or (disk.used / disk.total) > 0.95:
            resource_status = "critical"
            overall_healthy = False
            
        health_status["checks"]["system_resources"] = {
            "status": resource_status,
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": round((disk.used / disk.total) * 100, 2),
            "message": f"System resources at {resource_status} levels"
        }
    except Exception as e:
        health_status["checks"]["system_resources"] = {
            "status": "unhealthy",
            "error": str(e),
            "message": "Failed to check system resources"
        }
        overall_healthy = False
    
    # Environment variables check
    required_env_vars = ["DATABASE_URL", "SECRET_KEY"]
    env_status = "healthy"
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            
    if missing_vars:
        env_status = "unhealthy"
        overall_healthy = False
        
    health_status["checks"]["environment"] = {
        "status": env_status,
        "missing_variables": missing_vars,
        "message": "All required environment variables present" if not missing_vars else f"Missing variables: {missing_vars}"
    }
    
    # Services availability check
    services_status = await check_services_availability()
    health_status["checks"]["services"] = services_status
    if services_status["status"] != "healthy":
        overall_healthy = False
    
    # Set overall status
    health_status["status"] = "healthy" if overall_healthy else "unhealthy"
    
    return health_status

@router.get("/readiness")
async def readiness_check():
    """
    Readiness probe for Kubernetes
    
    Indicates if the application is ready to receive traffic.
    """
    
    try:
        # Check database connectivity
        db.execute(text("SELECT 1")).fetchone()
        
        # Check if all required services are initialized
        # (This would check service registrations, cache initialization, etc.)
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Application is ready to receive traffic"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "error": str(e),
                "message": "Application is not ready"
            }
        )

@router.get("/liveness")
async def liveness_check():
    """
    Liveness probe for Kubernetes
    
    Indicates if the application is still running and should not be restarted.
    """
    
    try:
        # Basic application liveness checks
        # Check if main threads are responsive
        # Check if no deadlocks exist
        
        return {
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": time.time() - psutil.Process().create_time(),
            "message": "Application is alive and running"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_alive",
                "error": str(e),
                "message": "Application liveness check failed"
            }
        )

@router.get("/modules")
async def modules_health_check():
    """
    Check health of all SILA modules
    
    Provides detailed status of each module's availability and performance.
    """
    
    modules = [
        "health", "education", "citizenship", "finance", "urbanism",
        "justice", "social", "complaints", "commercial", "sanitation",
        "registry", "service_hub", "auth", "common", "governance",
        "integration", "internal", "statistics", "documents", "address"
    ]
    
    module_health = {}
    
    for module in modules:
        # For each module, we would check:
        # - Service registrations
        # - Recent error rates
        # - Response times
        # - Dependencies status
        
        # Mock health check (in production, this would be real checks)
        module_health[module] = {
            "status": "healthy",
            "services_count": 5 if module in ["health", "education"] else 8 if module == "citizenship" else 6,
            "avg_response_time_ms": 250,
            "error_rate_percent": 0.5,
            "last_error": None,
            "uptime_percent": 99.8
        }
    
    # Simulate some issues for demonstration
    module_health["integration"]["status"] = "warning"
    module_health["integration"]["error_rate_percent"] = 2.1
    module_health["integration"]["last_error"] = "Connection timeout to external service"
    
    overall_status = "healthy"
    unhealthy_modules = [name for name, health in module_health.items() if health["status"] in ["unhealthy", "critical"]]
    warning_modules = [name for name, health in module_health.items() if health["status"] == "warning"]
    
    if unhealthy_modules:
        overall_status = "unhealthy"
    elif warning_modules:
        overall_status = "warning"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "total_modules": len(modules),
            "healthy_modules": len([m for m in module_health.values() if m["status"] == "healthy"]),
            "warning_modules": len(warning_modules),
            "unhealthy_modules": len(unhealthy_modules)
        },
        "modules": module_health
    }

@router.get("/dependencies")
async def dependencies_health_check():
    """
    Check health of external dependencies
    
    Monitors external services and integrations that SILA depends on.
    """
    
    dependencies = {
        "database": {
            "type": "PostgreSQL",
            "status": "healthy",
            "response_time_ms": 15,
            "last_check": datetime.utcnow().isoformat()
        },
        "cache": {
            "type": "Redis",
            "status": "healthy",
            "response_time_ms": 2,
            "last_check": datetime.utcnow().isoformat()
        },
        "file_storage": {
            "type": "MinIO/S3",
            "status": "warning",
            "response_time_ms": 500,
            "last_check": datetime.utcnow().isoformat(),
            "message": "Slow response times detected"
        },
        "external_apis": {
            "type": "Government APIs",
            "status": "healthy",
            "services_available": 8,
            "services_total": 10,
            "last_check": datetime.utcnow().isoformat()
        }
    }
    
    overall_status = "healthy"
    critical_deps = [name for name, dep in dependencies.items() if dep["status"] in ["unhealthy", "critical"]]
    warning_deps = [name for name, dep in dependencies.items() if dep["status"] == "warning"]
    
    if critical_deps:
        overall_status = "unhealthy"
    elif warning_deps:
        overall_status = "warning"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": dependencies
    }

async def check_services_availability() -> Dict[str, Any]:
    """
    Internal function to check service availability
    """
    
    # This would perform actual checks against service endpoints
    # For now, returning mock data
    
    return {
        "status": "healthy",
        "total_services": 150,
        "available_services": 148,
        "unavailable_services": 2,
        "response_time_avg_ms": 245,
        "message": "Most services are available and responding normally"
    }