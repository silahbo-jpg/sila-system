"""
Core Notification Module

This module handles all notification services:
- SMS notifications
- Email notifications
- Push notifications
- Webhook notifications

Key features:
- Template-based messaging
- Multi-channel delivery
- Retry logic and status tracking
- Bulk notifications
- Integration with citizen and payment systems
"""

from .services import NotificationService
from .providers import SMSProvider, EmailProvider, PushProvider, WebhookProvider
from .models import (
    NotificationCreate, NotificationUpdate, NotificationResponse,
    NotificationTemplateCreate, NotificationTemplateResponse,
    NotificationSearchFilters, BulkNotificationRequest
)
from .schemas import *

__all__ = [
    "NotificationService",
    "SMSProvider", "EmailProvider", "PushProvider", "WebhookProvider",
    "NotificationCreate", "NotificationUpdate", "NotificationResponse",
    "NotificationTemplateCreate", "NotificationTemplateResponse",
    "NotificationSearchFilters", "BulkNotificationRequest"
]