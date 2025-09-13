""
Base factory for all test data factories.

This module provides a BaseFactory class that all other factories should inherit from.
It includes common configurations and utilities for generating test data.
"""
import factory
from faker import Faker
from typing import Any, Dict, Type, TypeVar, Generic

# Configure Faker for consistent test data
fake = Faker()
Faker.seed(42)  # For deterministic test data

T = TypeVar('T')

class BaseFactory(factory.Factory, Generic[T]):
    """
    Base factory for all model factories.
    
    This factory provides common functionality for all model factories, including:
    - Automatic model instance creation
    - Support for both in-memory and persisted instances
    - Common field generators
    """
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class: Type[T], *args: Any, **kwargs: Any) -> T:
        """
        Create an instance of the model, with support for both in-memory and persisted instances.
        
        Args:
            model_class: The model class to instantiate
            *args: Positional arguments for model initialization
            **kwargs: Keyword arguments for model initialization
            
        Returns:
            An instance of the model class
        """
        # If using SQLAlchemy or another ORM, you can add persistence logic here
        # Example for SQLAlchemy:
        # from app.db.session import SessionLocal
        # db = SessionLocal()
        # instance = model_class(*args, **kwargs)
        # db.add(instance)
        # db.commit()
        # db.refresh(instance)
        # return instance
        return model_class(*args, **kwargs)
    
    @classmethod
    def build_dict(cls, **kwargs: Any) -> Dict[str, Any]:
        """
        Build a dictionary of attributes without creating a model instance.
        
        Args:
            **kwargs: Override any generated attributes
            
        Returns:
            Dictionary of generated attributes
        """
        return factory.build(dict, FACTORY_CLASS=cls, **kwargs)
    
    @classmethod
    def create_batch(cls, size: int, **kwargs: Any) -> list[T]:
        """
        Create multiple instances of the model.
        
        Args:
            size: Number of instances to create
            **kwargs: Override any generated attributes
            
        Returns:
            List of created model instances
        """
        return [cls.create(**kwargs) for _ in range(size)]

# Common field factories for reuse across models
class CommonFields:
    """Common field generators that can be reused across multiple factories."""
    
    @staticmethod
    def email() -> str:
        """Generate a unique email address."""
        return factory.LazyFunction(lambda: f"{fake.user_name()}.{fake.uuid4()[:8]}@example.com")
    
    @staticmethod
    def phone_number() -> str:
        """Generate a Brazilian phone number."""
        return factory.LazyFunction(lambda: f"+55 {fake.msisdn()[2:]}")
    
    @staticmethod
    def cpf() -> str:
        """Generate a valid Brazilian CPF."""
        def generate_cpf() -> str:
            cpf = [fake.random_digit() for _ in range(9)]
            
            # Calculate first verification digit
            total = sum((10 - i) * num for i, num in enumerate(cpf))
            digit = 11 - (total % 11)
            cpf.append(digit if digit < 10 else 0)
            
            # Calculate second verification digit
            total = sum((11 - i) * num for i, num in enumerate(cpf))
            digit = 11 - (total % 11)
            cpf.append(digit if digit < 10 else 0)
            
            return ''.join(map(str, cpf))
        
        return factory.LazyFunction(generate_cpf)
