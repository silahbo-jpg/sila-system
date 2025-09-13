"""
Factory for creating License test instances.

This module provides a LicenseFactory for generating test License instances with realistic fake data.
"""
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Any
from enum import Enum

import factory
from faker import Faker

from tests.factories.base_factory import BaseFactory
from tests.factories.service_factory import ServiceFactory
from tests.factories.citizen_factory import CitizenFactory

fake = Faker('pt_BR')

class LicenseStatus(str, Enum):
    DRAFT = "rascunho"
    UNDER_REVIEW = "em_analise"
    APPROVED = "aprovado"
    REJECTED = "rejeitado"
    ACTIVE = "ativo"
    EXPIRED = "expirado"
    REVOKED = "revogado"

class LicenseFactory(BaseFactory):
    """
    Factory for creating License instances for testing.
    
    Generates realistic license data with:
    - Unique license numbers
    - Realistic issue and expiration dates
    - Various statuses and metadata
    """
    
    class Meta:
        # This should be updated to point to your actual License model
        # Example: from app.models.license import License
        model = "License"  # Replace with actual License model import
        strategy = factory.BUILD_STRATEGY  # Don't persist by default
    
    # Core fields
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    license_number = factory.LazyFunction(
        lambda: f"LIC-{fake.unique.bothify(text='??-####-####')}"
    )
    
    # Relationships (these would be actual model instances in real usage)
    service_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    citizen_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    
    # Status and workflow
    status = factory.LazyFunction(
        lambda: fake.random_element(elements=list(LicenseStatus)).value
    )
    
    # Timing information
    application_date = factory.LazyFunction(
        lambda: fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc)
    )
    
    issue_date = factory.LazyAttribute(
        lambda o: o.application_date + timedelta(
            days=fake.random_int(min=1, max=30)
        ) if o.status in [LicenseStatus.APPROVED, LicenseStatus.ACTIVE, LicenseStatus.EXPIRED] 
        else None
    )
    
    expiration_date = factory.LazyAttribute(
        lambda o: o.issue_date + timedelta(
            days=fake.random_int(min=30, max=365)
        ) if o.issue_date else None
    )
    
    # License details
    category = factory.LazyFunction(
        lambda: fake.random_element(elements=(
            "ambiental", "sanitaria", "urbanistica", "fiscal", "outros"
        ))
    )
    
    validity_period = factory.LazyFunction(
        lambda: f"{fake.random_int(min=1, max=60)} meses"
    )
    
    # Documents and attachments
    documents = factory.LazyFunction(
        lambda: [
            {
                "type": "requerimento",
                "name": f"Requerimento_{fake.uuid4()}.pdf",
                "url": f"https://example.com/documents/{fake.uuid4()}",
                "uploaded_at": fake.date_time_this_year(tzinfo=timezone.utc).isoformat()
            },
            {
                "type": "documento_identidade",
                "name": f"RG_{fake.uuid4()}.pdf",
                "url": f"https://example.com/documents/{fake.uuid4()}",
                "uploaded_at": fake.date_time_this_year(tzinfo=timezone.utc).isoformat()
            }
        ]
    )
    
    # Fees and payments
    fees = factory.LazyFunction(
        lambda: [
            {
                "description": "Taxa de emissão",
                "amount": float(fake.random_number(digits=3, fix_len=False)) + 0.99,
                "currency": "BRL",
                "due_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
                "status": fake.random_element(elements=("pago", "pendente", "atrasado"))
            }
        ]
    )
    
    # Inspection and verification
    inspection_required = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=30))
    
    inspections = factory.LazyAttribute(
        lambda o: [
            {
                "date": (datetime.now(timezone.utc) - timedelta(days=fake.random_int(min=1, max=30))).isoformat(),
                "inspector": fake.name(),
                "status": fake.random_element(elements=("aprovado", "pendente", "reprovado")),
                "report_url": f"https://example.com/inspections/{fake.uuid4()}"
            }
        ] if o.inspection_required else []
    )
    
    # Metadata
    metadata = factory.LazyFunction(
        lambda: {
            "created_by": "system",
            "updated_by": "system",
            "workflow_steps": [
                {
                    "step": "submissao",
                    "status": "concluido",
                    "completed_at": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
                },
                {
                    "step": "analise",
                    "status": "em_andamento",
                    "started_at": (datetime.now(timezone.utc) - timedelta(days=4)).isoformat()
                }
            ]
        }
    )
    
    # Class methods for common scenarios
    @classmethod
    def create_draft(cls, **kwargs) -> 'License':
        """Create a license in draft status."""
        return cls.create(status=LicenseStatus.DRAFT.value, **kwargs)
    
    @classmethod
    def create_under_review(cls, **kwargs) -> 'License':
        """Create a license under review."""
        return cls.create(status=LicenseStatus.UNDER_REVIEW.value, **kwargs)
    
    @classmethod
    def create_active(cls, **kwargs) -> 'License':
        """Create an active license."""
        issue_date = kwargs.pop('issue_date', datetime.now(timezone.utc) - timedelta(days=30))
        return cls.create(
            status=LicenseStatus.ACTIVE.value,
            issue_date=issue_date,
            expiration_date=issue_date + timedelta(days=365),
            **kwargs
        )
    
    @classmethod
    def create_expired(cls, **kwargs) -> 'License':
        """Create an expired license."""
        issue_date = datetime.now(timezone.utc) - timedelta(days=400)
        expiration_date = issue_date + timedelta(days=365)
        return cls.create(
            status=LicenseStatus.EXPIRED.value,
            issue_date=issue_date,
            expiration_date=expiration_date,
            **kwargs
        )


# Convenience fixtures for tests
def create_license(**kwargs):
    """Create a standard license for testing."""
    return LicenseFactory.create(**kwargs)


def create_draft_license(**kwargs):
    """Create a license in draft status."""
    return LicenseFactory.create_draft(**kwargs)


def create_active_license(**kwargs):
    """Create an active license."""
    return LicenseFactory.create_active(**kwargs)


def create_expired_license(**kwargs):
    """Create an expired license."""
    return LicenseFactory.create_expired(**kwargs)
