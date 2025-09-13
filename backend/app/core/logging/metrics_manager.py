"""
Metrics manager for the application.

This module provides a centralized way to manage Prometheus metrics
and ensure they are only created once and properly cleaned up between tests.
"""
from typing import Dict, Optional, Type, TypeVar, Any
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    REGISTRY,
    CollectorRegistry,
)

T = TypeVar('T', Counter, Gauge, Histogram)

class MetricsManager:
    _instance = None
    _registry = None
    _metrics: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsManager, cls).__new__(cls)
            cls._registry = CollectorRegistry()
        return cls._instance

    @classmethod
    def get_or_create_metric(
        cls,
        metric_class: Type[T],
        name: str,
        documentation: str,
        labelnames: Optional[list] = None,
        **kwargs
    ) -> T:
        """Get an existing metric or create a new one if it doesn't exist."""
        if name in cls._metrics:
            return cls._metrics[name]

        # Ensure registry is used from kwargs or use our custom one
        if 'registry' not in kwargs:
            kwargs['registry'] = cls._registry

        metric = metric_class(
            name=name,
            documentation=documentation,
            labelnames=labelnames or [],
            **kwargs
        )
        cls._metrics[name] = metric
        return metric

    @classmethod
    def clear_metrics(cls):
        """Clear all registered metrics."""
        cls._metrics = {}
        # Unregister all collectors from the registry
        for collector in list(REGISTRY._collector_to_names.keys()):
            REGISTRY.unregister(collector)

# Convenience functions for common metric types
def get_or_create_counter(name: str, documentation: str, labelnames: Optional[list] = None, **kwargs) -> Counter:
    return MetricsManager().get_or_create_metric(
        Counter, name, documentation, labelnames, **kwargs
    )

def get_or_create_gauge(name: str, documentation: str, labelnames: Optional[list] = None, **kwargs) -> Gauge:
    return MetricsManager().get_or_create_metric(
        Gauge, name, documentation, labelnames, **kwargs
    )

def get_or_create_histogram(name: str, documentation: str, labelnames: Optional[list] = None, **kwargs) -> Histogram:
    return MetricsManager().get_or_create_metric(
        Histogram, name, documentation, labelnames, **kwargs
    )

def clear_all_metrics():
    """Clear all metrics. Should be called between tests."""
    MetricsManager().clear_metrics()
