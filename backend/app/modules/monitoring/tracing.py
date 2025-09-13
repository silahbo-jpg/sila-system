"""
Tracing Module

This module provides OpenTelemetry tracing functionality for the SILA system.
It sets up and manages distributed tracing across services.
"""

from typing import Any, Dict, Optional, Callable, TypeVar, Type
from functools import wraps
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
from opentelemetry.trace.status import Status, StatusCode

# Type variable for generic function wrapping
F = TypeVar('F', bound=Callable[..., Any])

class SilaTracing:
    """
    Centralized tracing management for SILA system.
    """
    
    def __init__(self, service_name: str = "sila-backend", service_version: str = "0.1.0"):
        self._tracer_provider = None
        self._meter_provider = None
        self._is_initialized = False
        self.service_name = service_name
        self.service_version = service_version
        self.resource = Resource.create({
            SERVICE_NAME: service_name,
            SERVICE_VERSION: service_version,
        })
    
    def initialize(self, jaeger_host: str = "localhost", jaeger_port: int = 6831, sample_rate: float = 1.0):
        """
        Initialize the tracing system.
        
        Args:
            jaeger_host: Jaeger agent host
            jaeger_port: Jaeger agent port
            sample_rate: Sampling rate (0.0 - 1.0)
        """
        if self._is_initialized:
            return
            
        # Create tracer provider
        sampler = ParentBased(TraceIdRatioBased(sample_rate))
        self._tracer_provider = TracerProvider(
            resource=self.resource,
            sampler=sampler
        )
        
        # Set up Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=jaeger_host,
            agent_port=jaeger_port,
        )
        
        # Add span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        self._tracer_provider.add_span_processor(span_processor)
        
        # Set the global tracer provider
        trace.set_tracer_provider(self._tracer_provider)
        
        # Add console exporter in development
        if True:  # You might want to make this conditional on environment
            console_exporter = ConsoleSpanExporter()
            self._tracer_provider.add_span_processor(
                BatchSpanProcessor(console_exporter)
            )
        
        self._is_initialized = True
        logging.info(f"Tracing initialized for {self.service_name} v{self.service_version}")
    
    @property
    def is_initialized(self) -> bool:
        """Check if tracing is initialized."""
        return self._is_initialized
    
    @property
    def tracer_provider(self):
        """Get the tracer provider."""
        return self._tracer_provider
    
    @property
    def meter_provider(self):
        """Get the meter provider."""
        return self._meter_provider
    
    def get_tracer(self, name: str = None) -> trace.Tracer:
        """
        Get a tracer instance.
        
        Args:
            name: Name for the tracer (defaults to service name)
            
        Returns:
            A tracer instance
        """
        if not self._is_initialized:
            self.initialize()
        return trace.get_tracer(name or self.service_name, self.service_version)

# Global instance
sila_tracing = SilaTracing()

def get_tracer(name: str = None) -> trace.Tracer:
    """
    Get a tracer instance from the global SILA tracing system.
    
    Args:
        name: Optional name for the tracer
        
    Returns:
        A tracer instance
    """
    return sila_tracing.get_tracer(name)

def trace_function(
    name: str = None,
    attributes: Dict[str, Any] = None,
    record_exception: bool = True,
    tracer: trace.Tracer = None
) -> Callable[[F], F]:
    """
    Decorator to trace function execution.
    
    Args:
        name: Span name (defaults to function name)
        attributes: Additional span attributes
        record_exception: Whether to record exceptions
        tracer: Tracer to use (defaults to global tracer)
        
    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal name, tracer
            
            if not name:
                name = f"{func.__module__}.{func.__qualname__}"
                
            if not tracer:
                tracer = get_tracer(func.__module__)
                
            with tracer.start_as_current_span(name) as span:
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, str(value))
                        
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if record_exception:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
                finally:
                    # Add any cleanup here
                    pass
                    
        return wrapper  # type: ignore
    return decorator
