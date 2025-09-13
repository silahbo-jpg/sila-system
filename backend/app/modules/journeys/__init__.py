"""
Journeys Module - Intelligent Civic Journey Orchestration

This module implements smart civic journeys that orchestrate multiple services
across different modules to provide complete citizen-centric workflows.

Example: "Birth of a Child" journey triggers:
- Registry: Birth certificate registration
- Health: Vaccination scheduling
- Social: Family support enrollment
"""

from fastapi import APIRouter

router = APIRouter()

__all__ = ["router"]