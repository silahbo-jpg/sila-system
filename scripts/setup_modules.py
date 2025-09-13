#!/usr/bin/env python3
"""
sila_dev System - Module Structure Setup Script

This script automates the creation of required module files and directories
based on the project's structure requirements.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = BASE_DIR / "backend"
APP_DIR = BACKEND_DIR / "app"
MODULES_DIR = APP_DIR / "modules"
TESTS_DIR = BASE_DIR / "tests" / "modules"

# Required module structure
MODULE_FILES = [
    "__init__.py",
    "models.py",
    "schemas.py",
    "crud.py",
    "services.py",
    "endpoints.py"
]

# Module templates
INIT_TEMPLATE = """# {module_name} module"""

MODEL_TEMPLATE = """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class {module_name_cap}Base(BaseModel):
    """Base model for {module_name}."""
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*

class {module_name_cap}Create({module_name_cap}Base):
    """Schema for creating a new {module_name}."""
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*

class {module_name_cap}Update({module_name_cap}Base):
    """Schema for updating a {module_name}."""
    Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*

class {module_name_cap}InDB({module_name_cap}Base):
    """Schema for {module_name} in database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
"""

SCHEMA_TEMPLATE = """from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import {module_name_cap}InDB

# Add your schemas here"""

CRUD_TEMPLATE = """from sqlalchemy.orm import Session
from . import models, schemas

def get_{module_name}(db: Session, {module_name}_id: int):
    """Get a single {module_name} by ID."""
    return db.query(models.{module_name_cap}).filter(models.{module_name_cap}.id == {module_name}_id).first()

def get_{module_name}s(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of {module_name}s with pagination."""
    return db.query(models.{module_name_cap}).offset(skip).limit(limit).all()

# Add more CRUD operations as needed"""

SERVICES_TEMPLATE = """from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas

def create_{module_name}(db: Session, {module_name}_data: dict):
    """Create a new {module_name}."""
    db_{module_name} = models.{module_name_cap}(**{module_name}_data)
    db.add(db_{module_name})
    db.commit()
    db.refresh(db_{module_name})
    return db_{module_name}

# Add more service functions as needed"""

ENDPOINTS_TEMPLATE = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from . import schemas, crud, services

router = APIRouter(
    prefix="/{module_name}s",
    tags=["{module_name}"],
    responses={{404: {{"description": "Not found"}}}},
)

@router.get("/", response_model=List[schemas.{module_name_cap}InDB])
def list_{module_name}s(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve {module_name}s."""
    {module_name}s = crud.get_{module_name}s(db, skip=skip, limit=limit)
    return {module_name}s

# Add more endpoints as needed"""

def create_module_structure(module_name: str):
    """Create directory structure and files for a module."""
    module_dir = MODULES_DIR / module_name
    test_dir = TESTS_DIR / module_name
    
    # Create directories
    module_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test file
    test_file = test_dir / f"test_{module_name}.py"
    if not test_file.exists():
        test_file.touch()
    
    # Format module name for class names
    module_name_cap = module_name.capitalize()
    
    # Create module files
    files_content = {
        "__init__.py": INIT_TEMPLATE.format(module_name=module_name),
        "models.py": MODEL_TEMPLATE.format(module_name=module_name, module_name_cap=module_name_cap),
        "schemas.py": SCHEMA_TEMPLATE.format(module_name=module_name, module_name_cap=module_name_cap),
        "crud.py": CRUD_TEMPLATE.format(module_name=module_name, module_name_cap=module_name_cap),
        "services.py": SERVICES_TEMPLATE.format(module_name=module_name, module_name_cap=module_name_cap),
        "endpoints.py": ENDPOINTS_TEMPLATE.format(module_name=module_name, module_name_cap=module_name_cap)
    }
    
    for filename, content in files_content.items():
        file_path = module_dir / filename
        if not file_path.exists() or file_path.stat().st_size == 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    # Update __init__.py with __all__
    init_file = module_dir / "__init__.py"
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(f'"""{module_name_cap} module."""\\n\n')
        f.write('__all__ = [\n')
        f.write('    "models",\n')
        f.write('    "schemas",\n')
        f.write('    "crud",\n')
        f.write('    "services",\n')
        f.write('    "endpoints",\n')
        f.write(']\n')

def main():
    """Main function to set up all modules."""
    # List of modules to set up
    modules = [
        "internal",
        "education",
        "social",
        "health",
        "reports",
        "appointments",
        "citizenship",
        "justice"
    ]
    
    print("🚀 Setting up module structure...")
    
    for module in modules:
        print(f"🔧 Setting up {module} module...")
        create_module_structure(module)
    
    print("✅ Module structure setup complete!")
    print(f"📁 Check the following directories:")
    print(f"   - Backend modules: {MODULES_DIR}")
    print(f"   - Tests: {TESTS_DIR}")

if __name__ == "__main__":
    main()


