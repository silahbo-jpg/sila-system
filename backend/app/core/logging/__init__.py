"""
Logging package for the SILA application.

This package contains logging configuration, middleware, and utilities
for structured logging and observability.
"""

# Import key components to make them available at the package level
from .structured_logging import (
    get_structured_logger,
    setup_structured_logging,
    logger
)

# Alias for backward compatibility
get_logger = get_structured_logger

from .metrics import setup_metrics, get_metrics
from .prometheus_metrics import PrometheusMetrics
from .observability_middleware import ObservabilityMiddleware

__all__ = [
    'get_structured_logger',
    'get_logger',  # Add the alias to __all__
    'setup_structured_logging',
    'logger',
    'setup_metrics',
    'get_metrics',
    'PrometheusMetrics',
    'ObservabilityMiddleware'
]
