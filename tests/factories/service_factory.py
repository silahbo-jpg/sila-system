""
Factory for creating Service test instances.

This module provides a ServiceFactory for generating test Service instances with realistic fake data.
"""
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from enum import Enum

import factory
from faker import Faker

from tests.factories.base_factory import BaseFactory

fake = Faker('pt_BR')

class ServiceStatus(str, Enum):
    DRAFT = "rascunho"
    UNDER_REVIEW = "em_analise"
    APPROVED = "aprovado"
    REJECTED = "rejeitado"
    ACTIVE = "ativo"
    INACTIVE = "inativo"
    SUSPENDED = "suspenso"

class ServiceFactory(BaseFactory):
    """
    Factory for creating Service instances for testing.
    
    Generates realistic service data with:
    - Unique codes and names
    - Realistic descriptions and requirements
    - Various statuses and metadata
    """
    
    class Meta:
        # This should be updated to point to your actual Service model
        # Example: from app.models.service import Service
        model = "Service"  # Replace with actual Service model import
        strategy = factory.BUILD_STRATEGY  # Don't persist by default
    
    # Core fields
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    code = factory.LazyFunction(lambda: f"SRV-{fake.unique.bothify(text='??-####')}")
    name = factory.LazyFunction(lambda: f"Serviço de {fake.catch_phrase()}")
    description = factory.LazyFunction(
        lambda: fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
    )
    
    # Status and visibility
    status = factory.LazyFunction(
        lambda: fake.random_element(elements=list(ServiceStatus)).value
    )
    is_public = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=80))
    
    # Timing information
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyAttribute(lambda o: o.created_at)
    effective_date = factory.LazyFunction(
        lambda: fake.date_time_between(start_date='-30d', end_date='+30d', tzinfo=timezone.utc)
    )
    expiration_date = factory.LazyAttribute(
        lambda o: o.effective_date + timedelta(days=fake.random_int(min=30, max=365))
    )
    
    # Service details
    category = factory.LazyFunction(
        lambda: fake.random_element(elements=(
            "licenciamento", "autorizacao", "certidao", "alvara", "outros"
        ))
    )
    
    requirements = factory.LazyFunction(
        lambda: [
            {"description": f"Documento de {fake.word().capitalize()}", "required": True},
            {"description": f"Comprovante de {fake.word()}", "required": fake.boolean()},
            {"description": f"Formulário de {fake.word()}", "required": True},
        ]
    )
    
    fees = factory.LazyFunction(
        lambda: [
            {
                "description": "Taxa de análise",
                "amount": float(fake.random_number(digits=3, fix_len=False)) + 0.99,
                "currency": "BRL"
            }
        ]
    )
    
    processing_time = factory.LazyFunction(
        lambda: f"{fake.random_int(min=1, max=30)} dias úteis"
    )
    
    responsible_department = factory.LazyFunction(
        lambda: fake.random_element(elements=(
            "Secretaria de Fazenda",
            "Secretaria de Meio Ambiente",
            "Secretaria de Urbanismo",
            "Secretaria de Saúde",
            "Secretaria de Obras",
        ))
    )
    
    # Metadata
    tags = factory.LazyFunction(
        lambda: [fake.word() for _ in range(fake.random_int(min=1, max=5))]
    )
    
    metadata = factory.LazyFunction(
        lambda: {
            "version": "1.0",
            "created_by": "system",
            "last_updated_by": "system",
        }
    )
    
    # Class methods for common scenarios
    @classmethod
    def create_draft(cls, **kwargs) -> 'Service':
        """Create a service in draft status."""
        return cls.create(status=ServiceStatus.DRAFT.value, **kwargs)
    
    @classmethod
    def create_under_review(cls, **kwargs) -> 'Service':
        """Create a service under review."""
        return cls.create(status=ServiceStatus.UNDER_REVIEW.value, **kwargs)
    
    @classmethod
    def create_active(cls, **kwargs) -> 'Service':
        """Create an active service."""
        return cls.create(status=ServiceStatus.ACTIVE.value, **kwargs)


# Convenience fixtures for tests
def create_service(**kwargs):
    """Create a standard service for testing."""
    return ServiceFactory.create(**kwargs)


def create_draft_service(**kwargs):
    """Create a service in draft status."""
    return ServiceFactory.create_draft(**kwargs)


def create_active_service(**kwargs):
    """Create an active service."""
    return ServiceFactory.create_active(**kwargs)
