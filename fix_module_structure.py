#!/usr/bin/env python3
"""
Module Structure Fixer

This script automates the fixing of common module structure issues in the SILA project.
It ensures all modules have the required structure for the backend services.
"""

import os
from pathlib import Path
from typing import List, Set, Dict

# Base directory for modules
BASE_DIR = Path(__file__).parent / "backend" / "app" / "modules"
MODULES = [
    'citizenship', 'justice', 'internal', 'reports', 'social',
    'education', 'appointments', 'health', 'commercial', 'urbanism',
    'common', 'complaints', 'sanitation', 'statistics'
]

# Template for __init__.py
INIT_TEMPLATE = """"""

# Template for model files
MODELS_TEMPLATE = """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Base(BaseModel):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
"""

# Template for CRUD files
CRUD_TEMPLATE = """from sqlalchemy.orm import Session
from . import models

class CRUDBase:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()
"""

# Template for services files
SERVICES_TEMPLATE = """from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from . import crud, models, schemas

class ServiceBase:
    def __init__(self, crud):
        self.crud = crud
"""

# Template for endpoints files
ENDPOINTS_TEMPLATE = """from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..dependencies import get_db
from . import services, schemas

router = APIRouter(prefix="/api/v1", tags=["module_name"])
"""

def ensure_init_file(module_path: Path) -> None:
    """Ensure __init__.py exists and has __all__"""
    init_file = module_path / "__init__.py"
    
    if not init_file.exists():
        print(f"Creating {init_file}")
        init_file.touch()
    
    # Add __all__ if not present
    content = init_file.read_text() if init_file.exists() else ""
    if "__all__" not in content:
        print(f"Adding __all__ to {init_file}")
        with open(init_file, 'a') as f:
            if content and not content.endswith('\n'):
                f.write('\n')
            f.write('\n__all__ = ["models", "schemas", "crud", "services", "endpoints"]\n')

def ensure_file_content(file_path: Path, template: str, module_name: str = None) -> None:
    """Ensure file exists and has content"""
    if not file_path.exists() or file_path.stat().st_size == 0:
        print(f"Creating/Updating {file_path}")
        content = template
        if module_name and "module_name" in template:
            content = template.replace("module_name", module_name)
        file_path.write_text(content)

def ensure_test_structure(module_name: str) -> None:
    """Ensure test directory and __init__.py exist"""
    test_dir = BASE_DIR.parent.parent / "tests" / "modules" / module_name
    test_init = test_dir / "__init__.py"
    
    if not test_dir.exists():
        print(f"Creating test directory: {test_dir}")
        test_dir.mkdir(parents=True, exist_ok=True)
    
    if not test_init.exists():
        print(f"Creating test __init__.py: {test_init}")
        test_init.touch()

def fix_module(module_name: str) -> None:
    """Fix structure for a single module"""
    print(f"\nFixing module: {module_name}")
    module_path = BASE_DIR / module_name
    
    # Ensure module directory exists
    module_path.mkdir(exist_ok=True)
    
    # Ensure __init__.py with __all__
    ensure_init_file(module_path)
    
    # Ensure standard files exist with content
    ensure_file_content(module_path / "models.py", MODELS_TEMPLATE)
    ensure_file_content(module_path / "crud.py", CRUD_TEMPLATE)
    ensure_file_content(module_path / "services.py", SERVICES_TEMPLATE)
    ensure_file_content(module_path / "endpoints.py", 
                       ENDPOINTS_TEMPLATE, module_name)
    
    # Ensure test structure
    ensure_test_structure(module_name)

def main():
    print("SILA Module Structure Fixer")
    print("=" * 50)
    
    # Ensure base directory exists
    if not BASE_DIR.exists():
        print(f"Error: Directory not found: {BASE_DIR}")
        return
    
    # Process each module
    for module in MODULES:
        fix_module(module)
    
    print("\nAll modules processed successfully!")

if __name__ == "__main__":
    main()

