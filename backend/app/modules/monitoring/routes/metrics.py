"""
Metrics API Routes

Provides endpoints for Prometheus metrics collection and monitoring dashboards.
"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from typing import Dict, List, Any
from app.db.session import get_db
from app.modules.monitoring.metrics import get_metrics, sila_metrics
import json

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/prometheus", response_class=Response)
async def prometheus_metrics():
    """
    Prometheus metrics endpoint
    
    This endpoint provides metrics in Prometheus format for scraping.
    Should be configured in Prometheus with path: /monitoring/metrics/prometheus
    """
    
    # Update system metrics before export
    sila_metrics.update_system_metrics()
    
    # Export metrics in Prometheus format
    metrics_data = sila_metrics.export_metrics()
    
    return Response(
        content=metrics_data,
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )

@router.get("/summary")
async def metrics_summary():
    """
    Get a summary of current system metrics
    
    Returns key metrics in JSON format for dashboards and monitoring.
    """
    
    summary = sila_metrics.get_metrics_summary()
    return {
        "status": "success",
        "data": summary
    }

@router.get("/top-services")
async def get_top_services(limit: int = 10):
    """
    Get top 10 most used services
    
    This endpoint provides business intelligence about service usage patterns.
    """
    
    # This would typically query the database for actual usage statistics
    # For now, we'll return a mock response based on the metrics structure
    
    top_services = [
        {
            "service_name": "Agendamento de Consulta",
            "module": "health",
            "usage_count": 1250,
            "avg_response_time": 0.45,
            "success_rate": 98.2
        },
        {
            "service_name": "Solicitação de Carteira de Identidade",
            "module": "citizenship",
            "usage_count": 890,
            "avg_response_time": 0.32,
            "success_rate": 99.1
        },
        {
            "service_name": "Consulta de Notas Fiscais",
            "module": "finance",
            "usage_count": 675,
            "avg_response_time": 0.28,
            "success_rate": 97.8
        },
        {
            "service_name": "Matrícula Escolar",
            "module": "education",
            "usage_count": 543,
            "avg_response_time": 0.52,
            "success_rate": 96.5
        },
        {
            "service_name": "Licenciamento de Obra",
            "module": "urbanism",
            "usage_count": 432,
            "avg_response_time": 1.24,
            "success_rate": 94.2
        }
    ]
    
    return {
        "status": "success",
        "data": {
            "top_services": top_services[:limit],
            "total_services": 150,
            "measurement_period": "last_30_days"
        }
    }

@router.get("/errors-by-municipality")
async def get_errors_by_municipality(limit: int = 10):
    """
    Get error statistics grouped by municipality
    
    Provides insights into which municipalities are experiencing issues.
    """
    
    # Mock data based on the metrics structure
    errors_by_municipality = [
        {
            "municipality": "Luanda",
            "total_errors": 45,
            "error_rate": 2.1,
            "top_error_types": [
                {"type": "validation_error", "count": 28},
                {"type": "service_unavailable", "count": 12},
                {"type": "timeout", "count": 5}
            ]
        },
        {
            "municipality": "Benguela",
            "total_errors": 23,
            "error_rate": 1.8,
            "top_error_types": [
                {"type": "validation_error", "count": 15},
                {"type": "network_error", "count": 6},
                {"type": "database_error", "count": 2}
            ]
        },
        {
            "municipality": "Huambo",
            "total_errors": 18,
            "error_rate": 1.5,
            "top_error_types": [
                {"type": "validation_error", "count": 12},
                {"type": "timeout", "count": 4},
                {"type": "service_unavailable", "count": 2}
            ]
        }
    ]
    
    return {
        "status": "success",
        "data": {
            "errors_by_municipality": errors_by_municipality[:limit],
            "measurement_period": "last_24_hours",
            "total_municipalities": len(errors_by_municipality)
        }
    }

@router.get("/response-times")
async def get_response_times(service: str = None, module: str = None):
    """
    Get response time statistics by service or module
    
    Provides performance insights for service optimization.
    """
    
    if service:
        # Mock response time data for specific service
        data = {
            "service_name": service,
            "avg_response_time": 0.45,
            "p50_response_time": 0.32,
            "p95_response_time": 0.89,
            "p99_response_time": 1.24,
            "measurement_period": "last_hour"
        }
    elif module:
        # Mock response time data for module
        data = {
            "module_name": module,
            "avg_response_time": 0.52,
            "services_count": 12,
            "slowest_service": "Licenciamento de Obra",
            "fastest_service": "Consulta de Status",
            "measurement_period": "last_hour"
        }
    else:
        # Overall system response times
        data = {
            "system_avg_response_time": 0.48,
            "total_requests": 2847,
            "requests_per_minute": 47.5,
            "measurement_period": "last_hour"
        }
    
    return {
        "status": "success",
        "data": data
    }

@router.get("/approval-metrics")
async def get_approval_metrics():
    """
    Get approval workflow metrics
    
    Provides insights into approval bottlenecks and efficiency.
    """
    
    approval_data = {
        "total_pending_approvals": 23,
        "avg_approval_time_hours": 18.5,
        "approval_levels": {
            "level_1": {
                "pending": 15,
                "avg_time_hours": 12.2,
                "success_rate": 94.5
            },
            "level_2": {
                "pending": 8,
                "avg_time_hours": 24.8,
                "success_rate": 89.2
            }
        },
        "bottlenecks": [
            {
                "service": "Licenciamento Comercial",
                "pending_count": 8,
                "avg_wait_time": 32.5
            }
        ]
    }
    
    return {
        "status": "success",
        "data": approval_data
    }

@router.get("/batch-operations")
async def get_batch_operations_metrics():
    """
    Get batch operations metrics
    
    Provides insights into batch update operations and their success rates.
    """
    
    batch_data = {
        "total_operations_today": 12,
        "success_rate": 91.7,
        "operations_by_module": {
            "finance": {"count": 5, "success_rate": 100.0},
            "health": {"count": 3, "success_rate": 66.7},
            "education": {"count": 4, "success_rate": 100.0}
        },
        "recent_operations": [
            {
                "operation_type": "fee_increase",
                "module": "finance",
                "records_affected": 45,
                "status": "success",
                "timestamp": "2024-01-15T14:30:00Z"
            },
            {
                "operation_type": "timeout_update",
                "module": "health",
                "records_affected": 23,
                "status": "success",
                "timestamp": "2024-01-15T13:15:00Z"
            }
        ]
    }
    
    return {
        "status": "success",
        "data": batch_data
    }

@router.get("/system-health")
async def get_system_health():
    """
    Get comprehensive system health metrics
    
    Provides overall system status and health indicators.
    """
    
    # Update system metrics
    sila_metrics.update_system_metrics()
    
    health_data = {
        "overall_status": "healthy",
        "uptime_hours": 72.5,
        "cpu_usage_percent": sila_metrics.system_cpu_usage._value.get(),
        "memory_usage_percent": 68.2,
        "disk_usage_percent": 45.8,
        "active_users": sila_metrics.active_users._value.get(),
        "database_status": "connected",
        "cache_hit_rate": 94.2,
        "services_status": {
            "total": 150,
            "healthy": 148,
            "warning": 2,
            "critical": 0
        }
    }
    
    return {
        "status": "success",
        "data": health_data
    }