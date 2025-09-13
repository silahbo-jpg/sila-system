"""
Test factories for SILA System.

This package contains factory classes for generating test data using factory_boy.
Each factory corresponds to a model in the application and provides a convenient
way to create test instances with realistic fake data.
"""
from tests.factories.base_factory import BaseFactory
from tests.factories.user_factory import UserFactory
from tests.factories.citizen_factory import CitizenFactory
from tests.factories.service_factory import ServiceFactory
from tests.factories.license_factory import LicenseFactory

__all__ = [
    'BaseFactory',
    'UserFactory',
    'CitizenFactory',
    'ServiceFactory',
    'LicenseFactory',
]
