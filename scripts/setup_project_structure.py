#!/usr/bin/env python3
"""
sila_dev System - Project Structure Setup Script

This script automates the creation of required module files and directories.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = BASE_DIR / "backend"
APP_DIR = BACKEND_DIR / "app"
MODULES_DIR = APP_DIR / "modules"
TESTS_DIR = BASE_DIR / "tests" / "modules"

# List of modules to create
MODULES = [
    "internal",
    "education",
    "social",
    "health",
    "reports",
    "appointments",
    "citizenship",
    "justice"
]

def create_file(path, content=""):
    """Create a file with the given content if it doesn't exist."""
    if not path.exists() or path.stat().st_size == 0:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Created {path.relative_to(BASE_DIR)}")
    else:
        print(f"  ⏩ {path.relative_to(BASE_DIR)} already exists")

def setup_module(module_name):
    """Set up a single module with all required files."""
    print(f"\\n🔧 Setting up {module_name} module...")
    
    # Create module directory
    module_dir = MODULES_DIR / module_name
    module_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test directory
    test_dir = TESTS_DIR / module_name
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_content = f'\"\\"\"{module_name.capitalize()} module.\"\"\"\n\n__all__ = [\n    "models",\n    "schemas",\n    "crud",\n    "services",\n    "endpoints"\n]'
    create_file(module_dir / "__init__.py", init_content)
    
    # Create models.py
    models_content = '"""Database models for {} module."""\
                   \n\nfrom sqlalchemy import Column, Integer, String, DateTime\nfrom sqlalchemy.sql import func\n\nfrom ...core.database import Base\n\n\nclass {}(Base):\n    """{} model."""\n    \n    __tablename__ = "{}"\n    \n    id = Column(Integer, primary_key=True, index=True)\n    created_at = Column(DateTime(timezone=True), server_default=func.now())\n    updated_at = Column(DateTime(timezone=True), onupdate=func.now())\n    # Add your model fields here'.format(
        module_name.capitalize(),
        module_name.capitalize(),
        module_name
    )
    create_file(module_dir / "models.py", models_content)
    
    # Create schemas.py
    schemas_content = '"""Pydantic schemas for {} module."""\
                    \n\nfrom pydantic import BaseModel\nfrom datetime import datetime\nfrom typing import Optional\n\n\nclass {0}Base(BaseModel):\n    """Base schema for {1}."""\n    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*\n\n\nclass {0}Create({0}Base):\n    """Schema for creating a new {1}."""\n    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*\n\n\nclass {0}Update({0}Base):\n    """Schema for updating a {1}."""\n    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*\n\n\nclass {0}InDB({0}Base):\n    """Schema for {1} in database."""\n    id: int\n    created_at: datetime\n    updated_at: datetime\n\n    class Config:\n        orm_mode = True'.format(
        module_name.capitalize(),
        module_name
    )
    create_file(module_dir / "schemas.py", schemas_content)
    
    # Create crud.py
    crud_content = '"""CRUD operations for {} module."""\
                 \n\nfrom sqlalchemy.orm import Session\nfrom . import models\n\n\ndef get_{0}(db: Session, {0}_id: int):\n    """Get a single {0} by ID."""\n    return db.query(models.{1}).filter(models.{1}.id == {0}_id).first()\n\n\ndef get_{0}s(db: Session, skip: int = 0, limit: int = 100):\n    """Get a list of {0}s with pagination."""\n    return db.query(models.{1}).offset(skip).limit(limit).all()\n\n\ndef create_{0}(db: Session, {0}_data: dict):\n    """Create a new {0}."""\n    db_{0} = models.{1}(**{0}_data)\n    db.add(db_{0})\n    db.commit()\n    db.refresh(db_{0})\n    return db_{0}'.format(
        module_name,
        module_name.capitalize()
    )
    create_file(module_dir / "crud.py", crud_content)
    
    # Create services.py
    services_content = '"""Business logic for {} module."""\
                     \n\nfrom fastapi import HTTPException, status\nfrom sqlalchemy.orm import Session\nfrom . import models, schemas\n\n\ndef create_{0}(db: Session, {0}_in: schemas.{1}Create):\n    """Create a new {0}."""\n    db_{0} = models.{1}(**{0}_in.dict())\n    db.add(db_{0})\n    db.commit()\n    db.refresh(db_{0})\n    return db_{0}'.format(
        module_name,
        module_name.capitalize()
    )
    create_file(module_dir / "services.py", services_content)
    
    # Create endpoints.py
    endpoints_content = '"""API endpoints for {} module."""\
                      \n\nfrom fastapi import APIRouter, Depends, HTTPException\nfrom sqlalchemy.orm import Session\nfrom typing import List\n\nfrom ...core.database import get_db\nfrom . import schemas, services\n\n\nrouter = APIRouter(\n    prefix="/{}",\n    tags=["{}"],\n    responses={{404: {{"description": "Not found"}}}},\n)\n\n\n@router.get("/", response_model=List[schemas.{}InDB])\nasync def read_{}s(\n    skip: int = 0, \n    limit: int = 100, \n    db: Session = Depends(get_db)\n):\n    """Retrieve {}""".\n    return services.get_{}s(db, skip=skip, limit=limit)'.format(
        f"{module_name}s",
        module_name,
        module_name.capitalize(),
        module_name,
        module_name,
        module_name
    )
    create_file(module_dir / "endpoints.py", endpoints_content)
    
    # Create test file
    test_content = '"""Tests for {} module."""\
                 \n\nimport pytest\nfrom fastapi.testclient import TestClient\nfrom sqlalchemy.orm import Session\n\n\n@pytest.fixture\ndef {0}_data():\n    return {{}}\n\n\ndef test_create_{0}(client: TestClient, db: Session, {0}_data: dict):\n    """Test creating a new {0}."""\n    response = client.post("/{1}/", json={0}_data)\n    assert response.status_code == 200\n    data = response.json()\n    assert "id" in data\n    assert data["id"] is not None'.format(
        module_name,
        f"{module_name}s"
    )
    create_file(test_dir / f"test_{module_name}.py", test_content)

def main():
    """Main function to set up all modules."""
    print("🚀 Setting up project structure...")
    
    # Create required base directories
    for directory in [MODULES_DIR, TESTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Set up each module
    for module in MODULES:
        setup_module(module)
    
    print("\\n✅ Project structure setup complete!")
    print("\nNext steps:")
    print("1. Run database migrations")
    print("2. Update model definitions in each module's models.py")
    print("3. Define your API schemas in schemas.py")
    print("4. Implement business logic in services.py")
    print("5. Add your API endpoints in endpoints.py")

if __name__ == "__main__":
    main()


