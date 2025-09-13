"""
Observability Middleware for SILA System

This middleware integrates OpenTelemetry tracing and Prometheus metrics
collection with the FastAPI application automatically.
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.modules.monitoring.tracing import sila_tracing, get_tracer
from app.modules.monitoring.metrics import sila_metrics
import json

logger = logging.getLogger(__name__)

class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically adds observability to all requests
    
    Features:
    - Automatic request tracing with OpenTelemetry
    - Prometheus metrics collection
    - Request/response logging
    - Performance monitoring
    - Error tracking
    """
    
    def __init__(self, app, collect_request_body: bool = False, collect_response_body: bool = False):
        super().__init__(app)
        self.collect_request_body = collect_request_body
        self.collect_response_body = collect_response_body
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with full observability"""
        
        start_time = time.time()
        
        # Extract request information
        method = request.method
        url_path = request.url.path
        user_agent = request.headers.get("user-agent", "unknown")
        client_ip = self._get_client_ip(request)
        
        # Determine module from path
        module = self._extract_module_from_path(url_path)
        
        # Create tracing span
        tracer = get_tracer()
        span = None
        
        if tracer:
            span = tracer.start_span(f"{method} {url_path}")
            
            # Add span attributes
            span.set_attribute("http.method", method)
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("http.route", url_path)
            span.set_attribute("user_agent.original", user_agent)
            span.set_attribute("client.address", client_ip)
            span.set_attribute("sila.module", module)
            
            # Add user information if available
            user_id = self._extract_user_id(request)
            if user_id:
                span.set_attribute("user.id", user_id)
                
            # Add municipality information if available
            municipality = self._extract_municipality(request)
            if municipality:
                span.set_attribute("sila.municipality", municipality)
        
        # Collect request body size
        request_size = 0
        if hasattr(request, "_body"):
            request_size = len(request._body) if request._body else 0
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate response time
            duration = time.time() - start_time
            
            # Get response information
            status_code = response.status_code
            response_size = 0
            
            if hasattr(response, 'body'):
                response_size = len(response.body) if response.body else 0
            
            # Record metrics
            self._record_metrics(
                method=method,
                endpoint=url_path,
                status_code=status_code,
                duration=duration,
                module=module,
                request_size=request_size,
                response_size=response_size,
                municipality=municipality,
                user_id=user_id
            )
            
            # Update span with response information
            if span:
                span.set_attribute("http.status_code", status_code)
                span.set_attribute("http.response.size", response_size)
                
                if status_code >= 400:
                    span.set_attribute("error", True)
                    if status_code >= 500:
                        from opentelemetry import trace
                        span.set_status(trace.Status(trace.StatusCode.ERROR, f"HTTP {status_code}"))
                    
                span.add_event("request_completed", {
                    "duration_ms": duration * 1000,
                    "response_size": response_size
                })
                
            # Log request completion
            self._log_request_completion(
                method, url_path, status_code, duration, user_id, municipality
            )
            
            return response
            
        except Exception as e:
            # Calculate duration even for errors
            duration = time.time() - start_time
            
            # Record error metrics
            self._record_error_metrics(
                method=method,
                endpoint=url_path,
                module=module,
                error=e,
                municipality=municipality
            )
            
            # Record exception in span
            if span:
                span.record_exception(e)
                from opentelemetry import trace
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                
            # Log error
            logger.error(
                f"Request failed: {method} {url_path} - {str(e)}",
                extra={
                    "method": method,
                    "url": url_path,
                    "duration": duration,
                    "error": str(e),
                    "user_id": user_id,
                    "municipality": municipality
                }
            )
            
            raise
            
        finally:
            # End tracing span
            if span:
                span.end()
                
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        # Check for forwarded headers first
        forwarded_ip = request.headers.get("X-Forwarded-For")
        if forwarded_ip:
            return forwarded_ip.split(",")[0].strip()
            
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
            
        # Fallback to client host
        return request.client.host if request.client else "unknown"
        
    def _extract_module_from_path(self, path: str) -> str:
        """Extract module name from URL path"""
        path_parts = path.strip('/').split('/')
        
        if len(path_parts) >= 3 and path_parts[0] == "api":
            # Skip version (v1, v2, etc.)
            if path_parts[1].startswith('v') or path_parts[1] == "latest":
                return path_parts[2] if len(path_parts) > 2 else "unknown"
            else:
                return path_parts[1]
        elif len(path_parts) >= 1:
            return path_parts[0]
            
        return "unknown"
        
    def _extract_user_id(self, request: Request) -> str:
        """Extract user ID from request (if authenticated)"""
        # Try to get from request state (if set by auth middleware)
        if hasattr(request.state, 'user'):
            user = request.state.user
            if hasattr(user, 'id'):
                return str(user.id)
                
        # Try to get from Authorization header (JWT)
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # In a real implementation, you would decode the JWT
            # For now, just return a placeholder
            return "jwt_user"
            
        return None
        
    def _extract_municipality(self, request: Request) -> str:
        """Extract municipality from request"""
        # Try to get from custom header
        municipality = request.headers.get("X-Municipality")
        if municipality:
            return municipality
            
        # Try to get from user object
        if hasattr(request.state, 'user'):
            user = request.state.user
            if hasattr(user, 'municipality'):
                return user.municipality
                
        # Try to extract from query parameters
        municipality_param = request.query_params.get("municipality")
        if municipality_param:
            return municipality_param
            
        return "unknown"
        
    def _record_metrics(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: float,
        module: str,
        request_size: int,
        response_size: int,
        municipality: str = None,
        user_id: str = None
    ):
        """Record request metrics"""
        
        try:
            # Record basic request metrics
            sila_metrics.record_request(
                method=method,
                endpoint=endpoint,
                status_code=status_code,
                duration=duration,
                module=module,
                request_size=request_size,
                response_size=response_size
            )
            
            # Record service usage if this is a service endpoint
            if self._is_service_endpoint(endpoint):
                service_name = self._extract_service_name(endpoint)
                user_type = "citizen" if user_id else "anonymous"
                
                sila_metrics.record_service_usage(
                    service_name=service_name,
                    module=module,
                    municipality=municipality or "unknown",
                    user_type=user_type
                )
                
        except Exception as e:
            logger.error(f"Failed to record metrics: {e}")
            
    def _record_error_metrics(
        self,
        method: str,
        endpoint: str,
        module: str,
        error: Exception,
        municipality: str = None
    ):
        """Record error-specific metrics"""
        
        try:
            error_type = type(error).__name__
            
            # Record error by municipality
            if municipality:
                service_name = self._extract_service_name(endpoint)
                sila_metrics.record_error_by_municipality(
                    municipality=municipality,
                    service_name=service_name,
                    error_type=error_type
                )
                
            # Record validation errors specifically
            if "validation" in error_type.lower() or "pydantic" in error_type.lower():
                service_name = self._extract_service_name(endpoint)
                sila_metrics.record_validation_error(
                    service_name=service_name,
                    field_name="unknown",  # Would need to extract from error details
                    error_type=error_type
                )
                
        except Exception as e:
            logger.error(f"Failed to record error metrics: {e}")
            
    def _is_service_endpoint(self, endpoint: str) -> bool:
        """Check if endpoint is a service endpoint"""
        service_indicators = [
            "/api/", "/health/", "/citizenship/", "/finance/", 
            "/education/", "/urbanism/", "/justice/", "/social/"
        ]
        return any(indicator in endpoint for indicator in service_indicators)
        
    def _extract_service_name(self, endpoint: str) -> str:
        """Extract service name from endpoint"""
        path_parts = endpoint.strip('/').split('/')
        
        # For API endpoints: /api/v1/module/service
        if len(path_parts) >= 4 and path_parts[0] == "api":
            return path_parts[3]
        elif len(path_parts) >= 2:
            return path_parts[-1]
            
        return "unknown_service"
        
    def _log_request_completion(
        self,
        method: str,
        path: str,
        status_code: int,
        duration: float,
        user_id: str = None,
        municipality: str = None
    ):
        """Log request completion"""
        
        log_data = {
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
            "user_id": user_id,
            "municipality": municipality
        }
        
        if status_code >= 400:
            logger.warning(f"Request completed with error: {method} {path}", extra=log_data)
        else:
            logger.info(f"Request completed: {method} {path}", extra=log_data)

def setup_observability_middleware(app):
    """
    Setup observability middleware for the FastAPI application
    
    This function should be called during application startup.
    """
    
    # Initialize tracing if not already done
    if not sila_tracing.is_initialized:
        try:
            sila_tracing.initialize(
                service_name="sila-system",
                service_version="1.0.0",
                enable_console_export=False,
                enable_prometheus=True
            )
            
            # Instrument the FastAPI app
            sila_tracing.instrument_fastapi(app)
            
            logger.info("OpenTelemetry tracing initialized and FastAPI instrumented")
            
        except Exception as e:
            logger.error(f"Failed to initialize tracing: {e}")
    
    # Add observability middleware
    app.add_middleware(
        ObservabilityMiddleware,
        collect_request_body=False,  # Set to True if you want to log request bodies
        collect_response_body=False  # Set to True if you want to log response bodies
    )
    
    logger.info("Observability middleware added to FastAPI application")