"""
Core Payment Module

This module handles payment integration with multiple providers:
- BNA (Banco Nacional de Angola)
- Unitel Money
- M-Pesa
- Other banks and payment systems

Key features:
- Multi-provider payment processing
- Secure transaction handling
- Payment status tracking
- Webhook/callback management
- Payment notifications
"""

from .services import PaymentService
from .providers import BNAProvider, UnitelMoneyProvider, MPesaProvider
from .models import (
    PaymentCreate, PaymentUpdate, PaymentResponse,
    PaymentProviderResponse, PaymentNotificationResponse,
    PaymentStatusUpdate, PaymentSearchFilters
)
from .schemas import *

__all__ = [
    "PaymentService",
    "BNAProvider", "UnitelMoneyProvider", "MPesaProvider",
    "PaymentCreate", "PaymentUpdate", "PaymentResponse",
    "PaymentProviderResponse", "PaymentNotificationResponse",
    "PaymentStatusUpdate", "PaymentSearchFilters"
]