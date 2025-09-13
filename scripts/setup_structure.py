#!/usr/bin/env python3
"""
sila_dev System - Project Structure Setup Script
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
MODULES = ["internal", "education", "social", "health", "reports", "appointments", "citizenship", "justice"]

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
    test_dir = TESTS_DIR / module_name
    
    # Create __init__.py
    init_content = f'"""{module_name.capitalize()} module."""\
                 '\\n\n__all__ = [\n    "models",\n    "schemas",\n    "crud",\n    "services",\n    "endpoints"\n]'
    create_file(module_dir / "__init__.py", init_content)
    
    # Create models.py
    models_content = f'"""Database models for {module_name} module."""\
                   '\\n\nfrom sqlalchemy import Column, Integer, String, DateTime\nfrom sqlalchemy.sql import func\n\nfrom ...core.database import Base\n\n\nclass ' + f'{module_name.capitalize()}' + '(Base):\\n    """' + f'{module_name.capitalize()}' + ' model."""\\n    \n    __tablename__ = "' + f'{module_name}' + '"\\n    \n    id = Column(Integer, primary_key=True, index=True)\n    created_at = Column(DateTime(timezone=True), server_default=func.now())\n    updated_at = Column(DateTime(timezone=True), onupdate=func.now())\n    # Add your model fields here'
    create_file(module_dir / "models.py", models_content)
    
    # Create schemas.py
    schemas_content = f'"""Pydantic schemas for {module_name} module."""\
                    '\\n\nfrom pydantic import BaseModel\nfrom datetime import datetime\nfrom typing import Optional\n\n\nclass ' + f'{module_name.capitalize()}' + 'Base(BaseModel):\\n    """Base schema for ' + f'{module_name}' + '."""\\n    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*\n\n\nclass ' + f'{module_name.capitalize()}' + 'Create(' + f'{module_name.capitalize()}' + 'Base):\\n    """Schema for creating a new ' + f'{module_name}' + '."""\\n    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*\n\n\nclass ' + f'{module_name.capitalize()}' + 'Update(' + f'{module_name.capitalize()}' + 'Base):\\n    """Schema for updating a ' + f'{module_name}' + '."""\\n    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*\n\n\nclass ' + f'{module_name.capitalize()}' + 'InDB(' + f'{module_name.capitalize()}' + 'Base):\\n    """Schema for ' + f'{module_name}' + ' in database."""\\n    id: int\n    created_at: datetime\n    updated_at: datetime\n\n    class Config:\n        orm_mode = True'
    create_file(module_dir / "schemas.py", schemas_content)
    
    # Create crud.py
    crud_content = f'"""CRUD operations for {module_name} module."""\
                 '\\n\nfrom sqlalchemy.orm import Session\nfrom . import models\n\n\ndef get_' + f'{module_name}' + '(db: Session, ' + f'{module_name}' + '_id: int):\\n    """Get a single ' + f'{module_name}' + ' by ID."""\\n    return db.query(models.' + f'{module_name.capitalize()}' + ').filter(models.' + f'{module_name.capitalize()}' + '.id == ' + f'{module_name}' + '_id).first()\\n\n\ndef get_' + f'{module_name}' + 's(db: Session, skip: int = 0, limit: int = 100):\\n    """Get a list of ' + f'{module_name}' + 's with pagination."""\\n    return db.query(models.' + f'{module_name.capitalize()}' + ').offset(skip).limit(limit).all()\\n\n\ndef create_' + f'{module_name}' + '(db: Session, ' + f'{module_name}' + '_data: dict):\\n    """Create a new ' + f'{module_name}' + '."""\\n    db_' + f'{module_name}' + ' = models.' + f'{module_name.capitalize()}' + '(**' + f'{module_name}' + '_data)\\n    db.add(db_' + f'{module_name}' + ')\\n    db.commit()\n    db.refresh(db_' + f'{module_name}' + ')\\n    return db_' + f'{module_name}'
    create_file(module_dir / "crud.py", crud_content)
    
    # Create services.py
    services_content = f'"""Business logic for {module_name} module."""\
                     '\\n\nfrom fastapi import HTTPException, status\nfrom sqlalchemy.orm import Session\nfrom . import models, schemas\n\n\ndef create_' + f'{module_name}' + '(db: Session, ' + f'{module_name}' + '_in: schemas.' + f'{module_name.capitalize()}' + 'Create):\\n    """Create a new ' + f'{module_name}' + '."""\\n    db_' + f'{module_name}' + ' = models.' + f'{module_name.capitalize()}' + '(**' + f'{module_name}' + '_in.dict())\\n    db.add(db_' + f'{module_name}' + ')\\n    db.commit()\n    db.refresh(db_' + f'{module_name}' + ')\\n    return db_' + f'{module_name}'
    create_file(module_dir / "services.py", services_content)
    
    # Create endpoints.py
    endpoints_content = f'"""API endpoints for {module_name} module."""\
                      '\\n\nfrom fastapi import APIRouter, Depends, HTTPException\nfrom sqlalchemy.orm import Session\nfrom typing import List\n\nfrom ...core.database import get_db\nfrom . import schemas, services\n\n\nrouter = APIRouter(\n    prefix="/' + f'{module_name}' + 's",\\n    tags=["' + f'{module_name}' + '"],\\n    responses={{404: {{"description": "Not found"}}}},\n)\n\n\n@router.get("/", response_model=List[schemas.' + f'{module_name.capitalize()}' + 'InDB])\\nasync def read_' + f'{module_name}' + 's(\\n    skip: int = 0, \n    limit: int = 100, \n    db: Session = Depends(get_db)\n):\n    """Retrieve ' + f'{module_name}' + 's""".\\n    return services.get_' + f'{module_name}' + 's(db, skip=skip, limit=limit)'
    create_file(module_dir / "endpoints.py", endpoints_content)
    
    # Create test file
    test_content = f'"""Tests for {module_name} module."""\
                 '\\n\nimport pytest\nfrom fastapi.testclient import TestClient\nfrom sqlalchemy.orm import Session\n\n\n@pytest.fixture\ndef ' + f'{module_name}' + '_data():\\n    return {{}}\n\n\ndef test_create_' + f'{module_name}' + '(client: TestClient, db: Session, ' + f'{module_name}' + '_data: dict):\\n    """Test creating a new ' + f'{module_name}' + '."""\\n    response = client.post("/' + f'{module_name}' + 's/", json=' + f'{module_name}' + '_data)\\n    assert response.status_code == 200\n    data = response.json()\n    assert "id" in data\n    assert data["id"] is not None'
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


