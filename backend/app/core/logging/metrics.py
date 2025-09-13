"""
Metrics collection for the application.

This module provides functionality to track and expose application metrics,
particularly focused on authentication and API usage.
"""

from typing import Dict, Optional, Any
from prometheus_client import Counter, Histogram, Gauge, start_http_server, generate_latest, REGISTRY
from fastapi import Response
import time
from functools import wraps
from starlette.requests import Request
from starlette.routing import Match
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client.core import CollectorRegistry
from prometheus_client.exposition import ThreadingWSGIServer
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server
import threading

# Create a custom registry
registry = CollectorRegistry()

# Disable default collectors except core ones
for collector in list(REGISTRY._collector_to_names):
    collector_name = getattr(collector, '__name__', '')
    if collector_name not in ('ProcessCollector', 'PlatformCollector', 'GCCollector'):
        try:
            REGISTRY.unregister(collector)
        except KeyError:
            pass

# Authentication metrics
AUTH_ATTEMPTS = Counter(
    'auth_login_attempts_total',
    'Total number of login attempts',
    ['method', 'status']
)

AUTH_SUCCESS = Counter(
    'auth_success_total',
    'Total number of successful logins',
    ['method']
)

AUTH_FAILURE = Counter(
    'auth_failure_total',
    'Total number of failed login attempts',
    ['method', 'reason']
)

PASSWORD_RESET_REQUESTS = Counter(
    'auth_password_reset_requests_total',
    'Total number of password reset requests'
)

PASSWORD_RESETS = Counter(
    'auth_password_resets_total',
    'Total number of successful password resets'
)

# User registration metrics
USER_REGISTRATIONS = Counter(
    'user_registrations_total',
    'Total number of user registrations'
)

# Token metrics
TOKEN_REFRESHES = Counter(
    'auth_token_refreshes_total',
    'Total number of token refresh attempts',
    ['status']
)

# Request metrics
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint', 'status_code']
)

REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Number of active HTTP requests',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'active_users_total',
    'Total number of active users',
    ['role']
)

# -------------------- Metric Tracking Functions --------------------

def track_auth_attempt(method: str):
    AUTH_ATTEMPTS.labels(method=method, status='attempt').inc()

def track_auth_success(method: str):
    AUTH_ATTEMPTS.labels(method=method, status='success').inc()
    AUTH_SUCCESS.labels(method=method).inc()

def track_auth_failure(method: str, reason: str):
    AUTH_ATTEMPTS.labels(method=method, status='failure').inc()
    AUTH_FAILURE.labels(method=method, reason=reason).inc()

def track_password_reset_request():
    PASSWORD_RESET_REQUESTS.inc()

def track_password_reset():
    PASSWORD_RESETS.inc()

def track_user_registration():
    USER_REGISTRATIONS.inc()

def track_token_refresh(success: bool = True):
    status = 'success' if success else 'failure'
    TOKEN_REFRESHES.labels(status=status).inc()

def track_request_latency(method: str, endpoint: str, status_code: int, duration: float):
    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).observe(duration)

def update_active_users(role: str, count: int):
    ACTIVE_USERS.labels(role=role).set(count)

# -------------------- Metrics Exposure --------------------

def get_metrics() -> bytes:
    return generate_latest(registry)

async def metrics_endpoint():
    return Response(
        content=get_metrics(),
        media_type=CONTENT_TYPE_LATEST
    )

def start_metrics_server(port: int = 8001):
    app = make_wsgi_app(registry)
    httpd = make_server('', port, app, ThreadingWSGIServer)
    print(f"✅ Metrics server started on port {port}")
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

def setup_metrics(port: int = 8001):
    """Initialize and start the Prometheus metrics server."""
    try:
        start_metrics_server(port)
    except Exception as e:
        print(f"⚠️ Failed to start metrics server: {e}")

def get_route_path(request: Request) -> str:
    for route in request.app.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            return route.path
    return request.url.path
