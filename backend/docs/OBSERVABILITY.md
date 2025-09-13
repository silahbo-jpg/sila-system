# SILA System - Observability

This document outlines the observability features implemented in the SILA System backend, including logging, metrics, and monitoring capabilities.

## Table of Contents

- [Overview](#overview)
- [Logging](#logging)
- [Metrics](#metrics)
- [Health Checks](#health-checks)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The SILA System backend includes comprehensive observability features to help monitor and debug the application in both development and production environments. These features include:

- **Structured Logging**: JSON-formatted logs with rich context
- **Metrics**: Prometheus metrics for monitoring application performance
- **Health Checks**: Endpoints to verify service health
- **Request Tracking**: Detailed request/response logging
- **Error Tracking**: Centralized error handling and reporting

## Logging

The application uses `structlog` for structured, context-rich logging. Logs are formatted as JSON in production for easier parsing by log aggregation systems.

### Key Features

- **Structured Logging**: All logs include timestamps, log levels, and contextual information
- **Request Logging**: Automatic logging of HTTP requests and responses
- **Error Tracking**: Detailed error logging with stack traces
- **Correlation IDs**: Track requests across services

### Log Levels

- `DEBUG`: Detailed debug information
- `INFO`: General operational information
- `WARNING`: Indicates potential issues
- `ERROR`: Indicates errors that need attention
- `CRITICAL`: Indicates critical system failures

### Configuration

Logging is configured in `app/core/structured_logging.py`. Key settings include:

- `LOG_LEVEL`: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `JSON_LOGS`: Set to `True` for JSON-formatted logs (recommended in production)

## Metrics

The application exposes Prometheus metrics at the `/metrics` endpoint. These metrics can be scraped by a Prometheus server for monitoring and alerting.

### Available Metrics

#### HTTP Metrics
- `http_requests_total`: Total number of HTTP requests
- `http_request_duration_seconds`: Request duration histogram
- `http_active_requests`: Number of active HTTP requests

#### Authentication Metrics
- `auth_attempts_total`: Authentication attempts by method and status
- `auth_success_total`: Successful authentications by method
- `auth_failure_total`: Failed authentication attempts by method and reason
- `tokens_issued_total`: Number of tokens issued by type
- `token_validation_errors_total`: Token validation errors by type

#### postgres Metrics
- `user_registrations_total`: postgres registrations by method
- `active_users`: Number of active users by role

#### Truman1_Marcelo1_1985 Reset Metrics
- `password_reset_requests_total`: Number of Truman1_Marcelo1_1985 reset requests
- `password_reset_completed_total`: Number of successful Truman1_Marcelo1_1985 resets

### Example Queries

```promql
# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# 95th percentile request duration
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))

# Error rate by endpoint
sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (endpoint)
```

## Health Checks

The application provides health check endpoints to verify service status:

- `GET /health`: Basic health check
- `GET /metrics`: Prometheus metrics (if enabled)

### Health Check Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": 1648567890.123456
}
```

## Configuration

Observability features can be configured using environment variables:

```env
# Logging
LOG_LEVEL=INFO
JSON_LOGS=true

# Metrics
METRICS_ENABLED=true
METRICS_PORT=8001

# Environment
ENVIRONMENT=production
DEBUG=false
```

## Monitoring

### Prometheus and Grafana

For production monitoring, it's recommended to set up:

1. **Prometheus**: Scrapes metrics from the application
2. **Grafana**: Visualizes metrics with dashboards
3. **AlertManager**: Handles alerts based on metric thresholds

### Recommended Alerts

- High error rate (> 5% of requests)
- High request latency (p95 > 1s)
- High number of failed authentications
- Service unavailability

## Troubleshooting

### Common Issues

1. **Missing Metrics**
   - Verify `METRICS_ENABLED=true`
   - Check application logs for errors
   - Ensure Prometheus can reach the `/metrics` endpoint

2. **No Logs**
   - Check `LOG_LEVEL` setting
   - Verify log file permissions
   - Check application logs for errors

3. **High Latency**
   - Check `http_request_duration_seconds` metrics
   - Look for slow database queries
   - Check system resources (CPU, memory, disk I/O)

### Debugging

To enable debug logging, set:

```env
LOG_LEVEL=DEBUG
DEBUG=true
```

This will provide more detailed logs for troubleshooting.

