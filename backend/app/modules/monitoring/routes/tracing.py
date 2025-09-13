"""
Tracing API Routes

Provides endpoints for OpenTelemetry tracing management and trace analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.modules.monitoring.tracing import get_tracer, sila_tracing, trace_function

router = APIRouter(prefix="/tracing", tags=["Distributed Tracing"])

@router.get("/status")
async def tracing_status():
    """
    Get OpenTelemetry tracing system status
    
    Returns information about the current tracing configuration and health.
    """
    
    return {
        "status": "active" if sila_tracing.is_initialized else "inactive",
        "tracer_provider": sila_tracing.tracer_provider is not None,
        "meter_provider": sila_tracing.meter_provider is not None,
        "instrumentation": {
            "fastapi": True,
            "sqlalchemy": True,
            "requests": True,
            "logging": True
        },
        "exporters": {
            "jaeger": bool(sila_tracing.tracer_provider),
            "console": False,  # Would check actual configuration
            "prometheus": bool(sila_tracing.meter_provider)
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/traces/recent")
async def get_recent_traces(
    limit: int = Query(default=10, ge=1, le=100),
    service_name: Optional[str] = Query(default=None),
    operation_name: Optional[str] = Query(default=None),
    min_duration_ms: Optional[int] = Query(default=None)
):
    """
    Get recent traces from the tracing system
    
    This would typically query Jaeger or another tracing backend.
    For demonstration, returns mock trace data.
    """
    
    # Mock trace data
    traces = [
        {
            "trace_id": "1a2b3c4d5e6f7890",
            "span_id": "abcdef1234567890",
            "operation_name": "GET /api/v1/health/agendamento-consulta",
            "service_name": "sila-system",
            "start_time": "2024-01-15T14:30:15.123Z",
            "duration_ms": 245,
            "status": "ok",
            "tags": {
                "http.method": "GET",
                "http.url": "/api/v1/health/agendamento-consulta",
                "http.status_code": 200,
                "user.id": "12345",
                "municipality": "Luanda"
            }
        },
        {
            "trace_id": "2b3c4d5e6f789012",
            "span_id": "bcdef12345678901",
            "operation_name": "POST /api/v1/citizenship/carteira-identidade",
            "service_name": "sila-system",
            "start_time": "2024-01-15T14:29:32.456Z",
            "duration_ms": 1240,
            "status": "ok",
            "tags": {
                "http.method": "POST",
                "http.url": "/api/v1/citizenship/carteira-identidade",
                "http.status_code": 201,
                "user.id": "67890",
                "municipality": "Benguela"
            }
        },
        {
            "trace_id": "3c4d5e6f78901234",
            "span_id": "cdef123456789012",
            "operation_name": "PUT /api/v1/finance/consulta-notas",
            "service_name": "sila-system",
            "start_time": "2024-01-15T14:28:18.789Z",
            "duration_ms": 89,
            "status": "error",
            "tags": {
                "http.method": "PUT",
                "http.url": "/api/v1/finance/consulta-notas",
                "http.status_code": 500,
                "error": True,
                "error.message": "Database connection timeout"
            }
        }
    ]
    
    # Apply filters
    filtered_traces = traces
    
    if service_name:
        filtered_traces = [t for t in filtered_traces if service_name in t["service_name"]]
    
    if operation_name:
        filtered_traces = [t for t in filtered_traces if operation_name in t["operation_name"]]
    
    if min_duration_ms:
        filtered_traces = [t for t in filtered_traces if t["duration_ms"] >= min_duration_ms]
    
    return {
        "status": "success",
        "data": {
            "traces": filtered_traces[:limit],
            "total_found": len(filtered_traces),
            "filters_applied": {
                "service_name": service_name,
                "operation_name": operation_name,
                "min_duration_ms": min_duration_ms
            }
        }
    }

@router.get("/traces/{trace_id}")
async def get_trace_detail(trace_id: str):
    """
    Get detailed information about a specific trace
    
    Returns complete span hierarchy and timing information.
    """
    
    # Mock detailed trace data
    if trace_id == "1a2b3c4d5e6f7890":
        trace_detail = {
            "trace_id": trace_id,
            "total_duration_ms": 245,
            "span_count": 4,
            "service_count": 1,
            "status": "ok",
            "spans": [
                {
                    "span_id": "abcdef1234567890",
                    "parent_span_id": None,
                    "operation_name": "GET /api/v1/health/agendamento-consulta",
                    "service_name": "sila-system",
                    "start_time": "2024-01-15T14:30:15.123Z",
                    "end_time": "2024-01-15T14:30:15.368Z",
                    "duration_ms": 245,
                    "tags": {
                        "http.method": "GET",
                        "http.status_code": 200,
                        "component": "fastapi"
                    }
                },
                {
                    "span_id": "bcdef12345678901",
                    "parent_span_id": "abcdef1234567890",
                    "operation_name": "database.query",
                    "service_name": "sila-system",
                    "start_time": "2024-01-15T14:30:15.145Z",
                    "end_time": "2024-01-15T14:30:15.289Z",
                    "duration_ms": 144,
                    "tags": {
                        "db.statement": "SELECT * FROM health_agendamento_consulta WHERE municipe_id = ?",
                        "db.type": "postgresql",
                        "component": "sqlalchemy"
                    }
                }
            ]
        }
        
        return {
            "status": "success",
            "data": trace_detail
        }
    else:
        raise HTTPException(status_code=404, detail="Trace not found")

@router.get("/services/performance")
async def get_services_performance(
    time_range: str = Query(default="1h", regex="^(1h|6h|24h|7d)$")
):
    """
    Get performance metrics for all services based on tracing data
    
    Analyzes trace data to provide service performance insights.
    """
    
    # Mock performance data
    services_performance = [
        {
            "service_name": "Agendamento de Consulta",
            "module": "health",
            "request_count": 1250,
            "avg_duration_ms": 245,
            "p95_duration_ms": 450,
            "p99_duration_ms": 890,
            "error_rate": 1.8,
            "throughput_rps": 0.35
        },
        {
            "service_name": "Carteira de Identidade",
            "module": "citizenship",
            "request_count": 890,
            "avg_duration_ms": 1240,
            "p95_duration_ms": 2100,
            "p99_duration_ms": 3200,
            "error_rate": 0.9,
            "throughput_rps": 0.25
        },
        {
            "service_name": "Consulta de Notas",
            "module": "finance",
            "request_count": 675,
            "avg_duration_ms": 89,
            "p95_duration_ms": 150,
            "p99_duration_ms": 280,
            "error_rate": 2.5,
            "throughput_rps": 0.19
        }
    ]
    
    return {
        "status": "success",
        "data": {
            "services": services_performance,
            "time_range": time_range,
            "measurement_period": f"last_{time_range}",
            "total_services": len(services_performance)
        }
    }

@router.get("/errors/analysis")
async def get_error_analysis(
    time_range: str = Query(default="1h", regex="^(1h|6h|24h|7d)$")
):
    """
    Analyze errors from tracing data
    
    Provides insights into error patterns, frequencies, and root causes.
    """
    
    error_analysis = {
        "time_range": time_range,
        "total_errors": 45,
        "error_rate": 2.1,
        "error_types": [
            {
                "type": "Database Timeout",
                "count": 18,
                "percentage": 40.0,
                "affected_services": ["Consulta de Notas", "Agendamento Consulta"],
                "avg_duration_ms": 5000
            },
            {
                "type": "Validation Error",
                "count": 15,
                "percentage": 33.3,
                "affected_services": ["Carteira Identidade", "Matrícula Escolar"],
                "avg_duration_ms": 50
            },
            {
                "type": "Service Unavailable",
                "count": 8,
                "percentage": 17.8,
                "affected_services": ["Licenciamento Obra"],
                "avg_duration_ms": 1000
            },
            {
                "type": "Network Error",
                "count": 4,
                "percentage": 8.9,
                "affected_services": ["External API Integration"],
                "avg_duration_ms": 3000
            }
        ],
        "top_error_traces": [
            {
                "trace_id": "3c4d5e6f78901234",
                "operation_name": "PUT /api/v1/finance/consulta-notas",
                "error_type": "Database Timeout",
                "duration_ms": 5240,
                "timestamp": "2024-01-15T14:28:18.789Z"
            }
        ]
    }
    
    return {
        "status": "success",
        "data": error_analysis
    }

@router.post("/manual-trace")
@trace_function(name="manual_trace_creation", attributes={"source": "api"})
async def create_manual_trace(
    operation_name: str,
    duration_ms: int,
    tags: Dict[str, Any] = None
):
    """
    Create a manual trace for testing purposes
    
    Useful for testing tracing infrastructure and creating sample traces.
    """
    
    tracer = get_tracer()
    if not tracer:
        raise HTTPException(status_code=503, detail="Tracing system not initialized")
    
    with tracer.start_as_current_span(operation_name) as span:
        # Add tags if provided
        if tags:
            for key, value in tags.items():
                span.set_attribute(key, str(value))
        
        # Simulate the operation duration
        import time
        time.sleep(duration_ms / 1000.0)  # Convert ms to seconds
        
        span.add_event("Manual trace completed")
    
    return {
        "status": "success",
        "message": f"Manual trace '{operation_name}' created successfully",
        "operation_name": operation_name,
        "duration_ms": duration_ms,
        "tags": tags or {}
    }

@router.get("/sampling/config")
async def get_sampling_config():
    """
    Get current trace sampling configuration
    
    Returns information about trace sampling rates and rules.
    """
    
    sampling_config = {
        "default_sampling_rate": 0.1,  # 10% sampling
        "service_sampling": {
            "health": 0.2,  # 20% for health services
            "finance": 0.15,  # 15% for financial services
            "citizenship": 0.25  # 25% for citizenship services
        },
        "operation_sampling": {
            "database.query": 0.05,  # 5% for database queries
            "external.api": 1.0  # 100% for external API calls
        },
        "adaptive_sampling": True,
        "max_traces_per_second": 100
    }
    
    return {
        "status": "success",
        "data": sampling_config
    }