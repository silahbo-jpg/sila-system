#!/usr/bin/env python3
"""
sila_dev System - Create Module Structure
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
MODULES = [
    "internal", "education", "social", "health", 
    "reports", "appointments", "citizenship", "justice"
]

def create_file(path, content=""):
    """Create a file with the given content."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def create_module(module_name):
    """Create all necessary files for a module."""
    module_dir = BASE_DIR / "backend" / "app" / "modules" / module_name
    test_dir = BASE_DIR / "tests" / "modules" / module_name
    
    # Create __init__.py
    init_content = f'''"""{module_name.capitalize()} module."""

__all__ = [
    "models",
    "schemas",
    "crud",
    "services",
    "endpoints"
]'''
    create_file(module_dir / "__init__.py", init_content)
    
    # Create models.py
    models_content = f'''"""Database models for {module_name} module."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from ...core.database import Base


class {module_name.capitalize()}(Base):
    """{module_name.capitalize()} model."""
    
    __tablename__ = "{module_name}"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Add your model fields here'''
    create_file(module_dir / "models.py", models_content)
    
    # Create schemas.py
    schemas_content = f'''"""Pydantic schemas for {module_name} module."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class {module_name.capitalize()}Base(BaseModel):
    """Base schema for {module_name}."""
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*


class {module_name.capitalize()}Create({module_name.capitalize()}Base):
    """Schema for creating a new {module_name}."""
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*


class {module_name.capitalize()}Update({module_name.capitalize()}Base):
    """Schema for updating a {module_name}."""
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*


class {module_name.capitalize()}InDB({module_name.capitalize()}Base):
    """Schema for {module_name} in database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True'''
    create_file(module_dir / "schemas.py", schemas_content)
    
    # Create crud.py
    crud_content = f'''"""CRUD operations for {module_name} module."""

from sqlalchemy.orm import Session
from . import models


def get_{module_name}(db: Session, {module_name}_id: int):
    """Get a single {module_name} by ID."""
    return db.query(models.{module_name.capitalize()}).filter(
        models.{module_name.capitalize()}.id == {module_name}_id
    ).first()


def get_{module_name}s(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of {module_name}s with pagination."""
    return db.query(models.{module_name.capitalize()}).offset(skip).limit(limit).all()


def create_{module_name}(db: Session, {module_name}_data: dict):
    """Create a new {module_name}."""
    db_{module_name} = models.{module_name.capitalize()}(**{module_name}_data)
    db.add(db_{module_name})
    db.commit()
    db.refresh(db_{module_name})
    return db_{module_name}'''
    create_file(module_dir / "crud.py", crud_content)
    
    # Create services.py
    services_content = f'''"""Business logic for {module_name} module."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas


def create_{module_name}(db: Session, {module_name}_in: schemas.{module_name.capitalize()}Create):
    """Create a new {module_name}."""
    db_{module_name} = models.{module_name.capitalize()}(**{module_name}_in.dict())
    db.add(db_{module_name})
    db.commit()
    db.refresh(db_{module_name})
    return db_{module_name}'''
    create_file(module_dir / "services.py", services_content)
    
    # Create endpoints.py
    endpoints_content = f'''"""API endpoints for {module_name} module."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from . import schemas, services


router = APIRouter(
    prefix="/{module_name}s",
    tags=["{module_name}"],
    responses={{404: {{"description": "Not found"}}}},
)


@router.get("/", response_model=List[schemas.{module_name.capitalize()}InDB])
async def read_{module_name}s(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Retrieve {module_name}s."""
    return services.get_{module_name}s(db, skip=skip, limit=limit)'''
    create_file(module_dir / "endpoints.py", endpoints_content)
    
    # Create test file
    test_content = f'''"""Tests for {module_name} module."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def {module_name}_data():
    return {{}}


def test_create_{module_name}(client: TestClient, db: Session, {module_name}_data: dict):
    """Test creating a new {module_name}."""
    response = client.post("/{module_name}s/", json={module_name}_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] is not None'''
    create_file(test_dir / f"test_{module_name}.py", test_content)

def main():
    """Create all module structures."""
    print("🚀 Creating module structure...")
    
    for module in MODULES:
        print(f"\n🔧 Setting up {module} module...")
        create_module(module)
    
    print("\n✅ Module structure created successfully!")
    print("\nNext steps:")
    print("1. Run database migrations")
    print("2. Update model definitions in each module's models.py")
    print("3. Define your API schemas in schemas.py")
    print("4. Implement business logic in services.py")
    print("5. Add your API endpoints in endpoints.py")

if __name__ == "__main__":
    main()


