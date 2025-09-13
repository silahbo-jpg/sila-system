""
Factory for creating Citizen test instances.

This module provides a CitizenFactory for generating test Citizen instances with realistic fake data.
"""
import uuid
from datetime import date, datetime, timezone
from typing import Optional, List, Dict, Any

import factory
from faker import Faker

from tests.factories.base_factory import BaseFactory, CommonFields

fake = Faker('pt_BR')  # Use Brazilian Portuguese for realistic data

class CitizenFactory(BaseFactory):
    """
    Factory for creating Citizen instances for testing.
    
    Generates realistic citizen data with:
    - Valid Brazilian CPF
    - Realistic names and addresses
    - Consistent demographic data
    """
    
    class Meta:
        # This should be updated to point to your actual Citizen model
        # Example: from app.models.citizen import Citizen
        model = "Citizen"  # Replace with actual Citizen model import
        strategy = factory.BUILD_STRATEGY  # Don't persist by default
    
    # Core identification
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    cpf = factory.LazyFunction(CommonFields.cpf)
    full_name = factory.LazyFunction(lambda: fake.name())
    social_name = factory.LazyAttribute(lambda o: o.full_name)
    
    # Personal information
    birth_date = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=16, maximum_age=100)
    )
    gender = factory.LazyFunction(
        lambda: fake.random_element(elements=('M', 'F', 'O', 'N'))
    )
    mother_name = factory.LazyFunction(lambda: fake.name_female())
    father_name = factory.LazyFunction(lambda: fake.name_male())
    
    # Contact information
    email = factory.LazyFunction(CommonFields.email)
    phone_number = factory.LazyFunction(CommonFields.phone_number)
    
    # Address information
    address_zip_code = factory.LazyFunction(lambda: fake.postcode())
    address_street = factory.LazyFunction(lambda: fake.street_name())
    address_number = factory.LazyFunction(lambda: str(fake.building_number()))
    address_complement = factory.LazyFunction(
        lambda: fake.random_element(elements=(
            '', 'Apto 101', 'Casa 2', 'Bloco B', 'Sala 3', 'Fundos'
        ))
    )
    address_neighborhood = factory.LazyFunction(lambda: fake.bairro())
    address_city = factory.LazyFunction(lambda: fake.city())
    address_state = factory.LazyFunction(lambda: fake.estado_sigla())
    
    # Documents
    rg_number = factory.LazyFunction(lambda: fake.rg())
    rg_issuer = factory.LazyFunction(lambda: 'SSP/' + fake.estado_sigla())
    rg_issue_date = factory.LazyFunction(
        lambda: fake.date_between(start_date='-20y', end_date='today')
    )
    
    # Status and metadata
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyAttribute(lambda o: o.created_at)
    
    # Additional data (can be used for flexible field storage)
    metadata = factory.LazyFunction(
        lambda: {}
    )
    
    # Class methods for common scenarios
    @classmethod
    def create_minimal(cls, **kwargs) -> 'Citizen':
        """Create a citizen with only required fields."""
        return cls.create(
            full_name=fake.name(),
            cpf=CommonFields.cpf(),
            birth_date=fake.date_of_birth(minimum_age=16, maximum_age=100),
            **kwargs
        )
    
    @classmethod
    def create_with_documents(cls, **kwargs) -> 'Citizen':
        """Create a citizen with complete document information."""
        return cls.create(
            rg_number=fake.rg(),
            rg_issuer='SSP/' + fake.estado_sigla(),
            rg_issue_date=fake.date_between(start_date='-20y', end_date='today'),
            **kwargs
        )
    
    @classmethod
    def create_with_address(cls, **kwargs) -> 'Citizen':
        """Create a citizen with complete address information."""
        return cls.create(
            address_zip_code=fake.postcode(),
            address_street=fake.street_name(),
            address_number=str(fake.building_number()),
            address_complement=fake.random_element(elements=('', 'Apto 101', 'Casa 2')),
            address_neighborhood=fake.bairro(),
            address_city=fake.city(),
            address_state=fake.estado_sigla(),
            **kwargs
        )


# Convenience fixtures for tests
def create_citizen(**kwargs):
    """Create a standard citizen for testing."""
    return CitizenFactory.create(**kwargs)


def create_minimal_citizen(**kwargs):
    """Create a citizen with only required fields."""
    return CitizenFactory.create_minimal(**kwargs)


def create_citizen_with_documents(**kwargs):
    """Create a citizen with complete document information."""
    return CitizenFactory.create_with_documents(**kwargs)


def create_citizen_with_address(**kwargs):
    """Create a citizen with complete address information."""
    return CitizenFactory.create_with_address(**kwargs)
