"""
Prometheus metrics configuration for the application.

This module defines and configures Prometheus metrics for monitoring the application.
It provides a centralized location for all metrics used throughout the application.
"""

# =========================
# Imports principais
# =========================
from typing import Dict, Optional, List, Type, Union
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    start_http_server as start_prometheus_server,
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
)
from prometheus_client.metrics import MetricWrapperBase
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from app.core.config import settings
from app.core.logging.structured_logging import get_structured_logger
from app.core.logging.metrics_manager import (
    get_or_create_counter,
    get_or_create_gauge,
    get_or_create_histogram,
    clear_all_metrics,
)

# =========================
# Definição de tipos
# =========================
MetricType = Union[Counter, Gauge, Histogram]
MetricLabels = Dict[str, str]

# =========================
# Classe principal
# =========================
class PrometheusMetrics:
    """A class to manage Prometheus metrics for the application.

    This class provides a centralized way to manage and access all Prometheus metrics
    used throughout the application.
    """

    def __init__(self):
        """Initialize the Prometheus metrics manager."""
        self.metrics: Dict[str, MetricType] = {}

    def get_metric(self, name: str) -> Optional[MetricType]:
        """Get a metric by name."""
        return self.metrics.get(name)

    def register_metric(self, metric: MetricType) -> None:
        """Register a new metric."""
        self.metrics[metric._name] = metric

    def get_or_create_metric(
        self,
        metric_class: Type[MetricType],
        name: str,
        documentation: str,
        labelnames: Optional[List[str]] = None,
        **kwargs,
    ) -> MetricType:
        """Get an existing metric or create it if it doesn't exist."""
        if name in self.metrics:
            return self.metrics[name]

        labelnames = labelnames or []
        metric = metric_class(name, documentation, labelnames=labelnames, **kwargs)
        self.register_metric(metric)
        return metric


# =========================
# Configuração de logger
# =========================
logger = get_structured_logger(__name__)

# =========================
# Definição de métricas
# =========================
REQUEST_LATENCY = get_or_create_histogram(
    name="http_request_duration_seconds",
    documentation="Request latency in seconds",
    labelnames=["method", "endpoint", "status_code"],
    buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)

REQUEST_COUNTER = get_or_create_counter(
    name="http_requests_total",
    documentation="Total number of HTTP requests",
    labelnames=["method", "endpoint", "status_code"],
)

ACTIVE_REQUESTS = get_or_create_gauge(
    name="http_active_requests",
    documentation="Number of active HTTP requests",
    labelnames=["method", "endpoint"],
)

AUTH_ATTEMPTS = get_or_create_counter(
    name="auth_attempts_total",
    documentation="Total number of authentication attempts",
    labelnames=["method", "status"],
)

AUTH_SUCCESS = get_or_create_counter(
    name="auth_success_total",
    documentation="Total number of successful authentications",
    labelnames=["method"],
)

AUTH_FAILURE = get_or_create_counter(
    name="auth_failure_total",
    documentation="Total number of failed authentication attempts",
    labelnames=["method", "reason"],
)

USER_REGISTRATIONS = get_or_create_counter(
    name="user_registrations_total",
    documentation="Total number of user registrations",
    labelnames=["method"],
)

ACTIVE_USERS = get_or_create_gauge(
    name="active_users",
    documentation="Number of active users",
    labelnames=["role"],
)

PASSWORD_RESET_REQUESTS = get_or_create_counter(
    name="password_reset_requests_total",
    documentation="Total number of password reset requests",
)

PASSWORD_RESET_COMPLETED = get_or_create_counter(
    name="password_reset_completed_total",
    documentation="Total number of successful password resets",
)

TOKEN_ISSUED = get_or_create_counter(
    name="tokens_issued_total",
    documentation="Total number of tokens issued",
    labelnames=["token_type"],
)

TOKEN_VALIDATION_ERRORS = get_or_create_counter(
    name="token_validation_errors_total",
    documentation="Total number of token validation errors",
    labelnames=["error_type"],
)

# =========================
# Funções de rastreamento
# =========================
def track_request_duration(
    method: str,
    endpoint: str,
    status_code: int,
    duration: float,
) -> None:
    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint,
        status_code=str(status_code),
    ).observe(duration)


def track_auth_attempt(
    method: str,
    status: str = "attempt",
    **labels: str,
) -> None:
    AUTH_ATTEMPTS.labels(method=method, status=status).inc()
    if status == "success":
        AUTH_SUCCESS.labels(method=method).inc()
    elif status == "failure" and "reason" in labels:
        AUTH_FAILURE.labels(method=method, reason=labels["reason"]).inc()


def track_user_registration(method: str = "email") -> None:
    USER_REGISTRATIONS.labels(method=method).inc()


def track_token_issue(token_type: str = "access") -> None:
    TOKEN_ISSUED.labels(token_type=token_type).inc()


def track_token_validation_error(error_type: str) -> None:
    TOKEN_VALIDATION_ERRORS.labels(error_type=error_type).inc()


def track_password_reset_request() -> None:
    PASSWORD_RESET_REQUESTS.inc()


def track_password_reset_complete() -> None:
    PASSWORD_RESET_COMPLETED.inc()


def update_active_users(role: str, delta: int = 1) -> None:
    ACTIVE_USERS.labels(role=role).inc(delta)


def get_metrics() -> bytes:
    return generate_latest()


def start_http_server(port: Optional[int] = None) -> None:
    if port is None:
        port = settings.METRICS_PORT
    try:
        start_prometheus_server(port)
        logger.info("Prometheus metrics server started", port=port, metrics_path=settings.METRICS_PATH)
    except Exception as e:
        logger.error("Failed to start Prometheus metrics server", error=str(e), port=port, exc_info=True)


async def metrics_endpoint(_: Request) -> Response:
    return Response(
        content=get_metrics(),
        status_code=HTTP_200_OK,
        media_type=CONTENT_TYPE_LATEST,
    )


def get_metric(metric_name: str) -> Optional[MetricWrapperBase]:
    return REGISTRY._names_to_collectors.get(metric_name)


def get_metric_value(metric_name: str, labels: Optional[MetricLabels] = None) -> float:
    metric = get_metric(metric_name)
    if metric is None:
        raise ValueError(f"Metric '{metric_name}' not found")
    if labels:
        return metric.labels(**labels)._value.get()
    return metric._value.get()


# =========================
# Exportação
# =========================
__all__ = [
    "PrometheusMetrics",
    "REQUEST_LATENCY",
    "REQUEST_COUNTER",
    "ACTIVE_REQUESTS",
    "AUTH_ATTEMPTS",
    "AUTH_SUCCESS",
    "AUTH_FAILURE",
    "USER_REGISTRATIONS",
    "ACTIVE_USERS",
    "PASSWORD_RESET_REQUESTS",
    "PASSWORD_RESET_COMPLETED",
    "TOKEN_ISSUED",
    "TOKEN_VALIDATION_ERRORS",
    "track_request_duration",
    "track_auth_attempt",
    "track_user_registration",
    "track_token_issue",
    "track_token_validation_error",
    "track_password_reset_request",
    "track_password_reset_complete",
    "update_active_users",
    "get_metrics",
    "start_http_server",
    "metrics_endpoint",
    "get_metric",
    "get_metric_value",
]
