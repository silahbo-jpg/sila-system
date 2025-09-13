"""
Metrics collection and monitoring utilities.

This module provides functions for collecting and exposing system metrics
for monitoring and observability.
"""

from typing import Dict, Any
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Initialize metrics
sila_metrics = {
    'requests_total': 0,
    'errors_total': 0,
    'active_connections': 0,
    'response_time_seconds': {}
}

def get_metrics() -> Dict[str, Any]:
    """
    Get current metrics snapshot.
    
    Returns:
        Dict containing current metric values
    """
    return sila_etrics

def increment_counter(metric_name: str, value: int = 1) -> None:
    """
    Increment a counter metric.
    
    Args:
        metric_name: Name of the metric to increment
        value: Value to increment by (default: 1)
    """
    if metric_name in sila_metrics and isinstance(sila_metrics[metric_name], (int, float)):
        sila_metrics[metric_name] += value

def set_gauge(metric_name: str, value: float) -> None:
    """
    Set a gauge metric value.
    
    Args:
        metric_name: Name of the gauge metric
        value: Value to set
    """
    if metric_name in sila_metrics:
        sila_metrics[metric_name] = value

def record_response_time(service: str, response_time: float) -> None:
    """
    Record response time for a service.
    
    Args:
        service: Name of the service
        response_time: Response time in seconds
    """
    if 'response_time_seconds' not in sila_metrics:
        sila_metrics['response_time_seconds'] = {}
    
    if service not in sila_metrics['response_time_seconds']:
        sila_metrics['response_time_seconds'][service] = []
    
    sila_metrics['response_time_seconds'][service].append(response_time)
    
    # Keep only the last 1000 samples per service
    if len(sila_metrics['response_time_seconds'][service]) > 1000:
        sila_metrics['response_time_seconds'][service] = sila_metrics['response_time_seconds'][service][-1000:]
