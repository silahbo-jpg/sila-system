#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enhanced Service Creation Script for SILA System

This script creates new services with automatic:
- Form schema generation from Pydantic models
- i18n synchronization (PT/EN translations)
- Dynamic service registration
- Frontend integration
"""

import os
import sys
import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
MODULES_DIR = BACKEND_DIR / "app" / "modules"
LOCALES_DIR = FRONTEND_DIR / "src" / "locales"

# Service template with form schema generation
SERVICE_TEMPLATE = '''
"""
{service_name} Service Module

Auto-generated service with dynamic form schema and i18n support.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.services import ServiceDefinition, FormSchema, FormField, FieldType

router = APIRouter()

# Service form schema definition
class {service_class_name}Request(BaseModel):
    """Request schema for {service_name} service"""
{form_fields}

    class Config:
        json_schema_extra = {{
            "example": {{
{form_example}
            }}
        }}

# Response schema
class {service_class_name}Response(BaseModel):
    """Response schema for {service_name} service"""
    id: str
    reference_number: str
    status: str
    created_at: datetime
    estimated_completion: Optional[str] = None

# Auto-generated form schema
FORM_SCHEMA = FormSchema(
    title="{service_display_name}",
    description="{service_description}",
    fields=[
{schema_fields}
    ],
    submit_button_text="Submit Request",
    cancel_button_text="Cancel"
)

# Service definition for dynamic registration
SERVICE_DEFINITION = ServiceDefinition(
    id="{service_id}",
    name="{service_display_name}",
    description="{service_description}",
    module="{module_name}",
    icon="{service_icon}",
    roles={service_roles},
    status="active",
    api_endpoint="/api/v1/{module_name}/{service_id}",
    form_schema=FORM_SCHEMA,
    translations={{
        "en": {{
            "name": "{service_display_name_en}",
            "description": "{service_description_en}"
        }},
        "pt": {{
            "name": "{service_display_name}",
            "description": "{service_description}"
        }}
    }},
    metadata={{
        "category": "{service_category}",
        "estimated_time": "{estimated_time}",
        "fee": "{service_fee}",
        "required_documents": {required_documents},
        "municipality_specific": {municipality_specific},
        "online_only": True
    }}
)

@router.post("/{service_id}", response_model={service_class_name}Response)
async def create_{service_id}_request(
    request: {service_class_name}Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new {service_name} request"""
    try:
        # Generate reference number
        import uuid
        reference_number = f"{service_id.upper()}_{uuid.uuid4().hex[:8].upper()}"
        
        # Process the request (implement your business logic here)
        # This is where you would save to database, validate documents, etc.
        
        return {service_class_name}Response(
            id=str(uuid.uuid4()),
            reference_number=reference_number,
            status="submitted",
            created_at=datetime.utcnow(),
            estimated_completion="{estimated_time}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing {service_name} request: {{str(e)}}"
        )

@router.get("/{service_id}/schema")
async def get_{service_id}_schema():
    """Get the form schema for {service_name} service"""
    return FORM_SCHEMA

@router.get("/{service_id}/definition")
async def get_{service_id}_definition():
    """Get the service definition for {service_name}"""
    return SERVICE_DEFINITION
'''

def create_form_field_definition(field_name: str, field_type: str, field_config: Dict[str, Any]) -> str:
    """Generate form field definition code"""
    field_class = field_config.get('field_class', 'str')
    required = field_config.get('required', False)
    default = field_config.get('default', 'None')
    description = field_config.get('description', f'{field_name.replace("_", " ").title()}')
    
    if required:
        if default != 'None':
            return f'    {field_name}: {field_class} = Field(default={default}, description="{description}")'
        else:
            return f'    {field_name}: {field_class} = Field(..., description="{description}")'
    else:
        return f'    {field_name}: Optional[{field_class}] = Field(default={default}, description="{description}")'

def create_schema_field_definition(field_name: str, field_type: str, field_config: Dict[str, Any]) -> str:
    """Generate schema field definition for FormField"""
    label = field_config.get('label', field_name.replace('_', ' ').title())
    required = field_config.get('required', False)
    placeholder = field_config.get('placeholder', '')
    help_text = field_config.get('help_text', '')
    options = field_config.get('options', [])
    
    schema_field = f'''        FormField(
            name="{field_name}",
            label="{label}",
            type=FieldType.{field_type.upper()},
            required={required}'''
    
    if placeholder:
        schema_field += f',\n            placeholder="{placeholder}"'
    if help_text:
        schema_field += f',\n            help_text="{help_text}"'
    if options:
        options_str = str(options).replace("'", '"')
        schema_field += f',\n            options={options_str}'
    
    schema_field += '\n        )'
    return schema_field

def update_translations(service_id: str, translations: Dict[str, Dict[str, str]]):
    """Update frontend translation files"""
    for lang, trans in translations.items():
        locale_file = LOCALES_DIR / f"{lang}.json"
        
        if locale_file.exists():
            with open(locale_file, 'r', encoding='utf-8') as f:
                locale_data = json.load(f)
        else:
            locale_data = {}
        
        # Create services section if it doesn't exist
        if 'services' not in locale_data:
            locale_data['services'] = {}
        
        # Add service translations
        locale_data['services'][service_id] = trans
        
        # Write back to file
        with open(locale_file, 'w', encoding='utf-8') as f:
            json.dump(locale_data, f, indent=2, ensure_ascii=False)
        
        print(f"Updated {lang}.json with translations for {service_id}")

def create_service(
    service_id: str,
    service_name: str,
    service_name_en: str,
    description: str,
    description_en: str,
    module_name: str,
    category: str,
    fields: Dict[str, Dict[str, Any]],
    **kwargs
):
    """Create a new service with all necessary files and configurations"""
    
    # Prepare service data
    service_class_name = ''.join(word.capitalize() for word in service_id.split('_'))
    
    # Generate form fields code
    form_fields = []
    form_example = []
    schema_fields = []
    
    for field_name, field_config in fields.items():
        field_type = field_config.get('type', 'string')
        form_fields.append(create_form_field_definition(field_name, field_type, field_config))
        
        # Example value for the field
        example_value = field_config.get('example', f'example_{field_name}')
        if field_config.get('field_class') == 'int':
            example_value = field_config.get('example', 123)
        elif field_config.get('field_class') == 'bool':
            example_value = field_config.get('example', True)
        
        form_example.append(f'                "{field_name}": {json.dumps(example_value)}')
        
        # Schema field
        schema_fields.append(create_schema_field_definition(field_name, field_type, field_config))
    
    # Prepare template variables
    template_vars = {
        'service_name': service_name,
        'service_class_name': service_class_name,
        'service_id': service_id,
        'service_display_name': service_name,
        'service_display_name_en': service_name_en,
        'service_description': description,
        'service_description_en': description_en,
        'module_name': module_name,
        'service_icon': kwargs.get('icon', 'document-text'),
        'service_roles': kwargs.get('roles', ['citizen', 'staff']),
        'service_category': category,
        'estimated_time': kwargs.get('estimated_time', '3-5 business days'),
        'service_fee': kwargs.get('fee', 'Free'),
        'required_documents': kwargs.get('required_documents', []),
        'municipality_specific': kwargs.get('municipality_specific', False),
        'form_fields': '\n'.join(form_fields),
        'form_example': ',\n'.join(form_example),
        'schema_fields': ',\n'.join(schema_fields)
    }
    
    # Create module directory if it doesn't exist
    module_dir = MODULES_DIR / module_name
    module_dir.mkdir(exist_ok=True)
    
    # Create service file
    service_file = module_dir / f"{service_id}_service.py"
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(SERVICE_TEMPLATE.format(**template_vars))
    
    print(f"Created service file: {service_file}")
    
    # Update translations
    translations = {
        'en': {
            'name': service_name_en,
            'description': description_en,
            **{f'{field_name}_label': field_config.get('label_en', field_config.get('label', field_name.replace('_', ' ').title())) 
               for field_name, field_config in fields.items()}
        },
        'pt': {
            'name': service_name,
            'description': description,
            **{f'{field_name}_label': field_config.get('label', field_name.replace('_', ' ').title()) 
               for field_name, field_config in fields.items()}
        }
    }
    
    update_translations(service_id, translations)
    
    # Update main module router (if exists)
    endpoints_file = module_dir / "endpoints.py"
    if endpoints_file.exists():
        with open(endpoints_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import for the new service
        import_line = f"from .{service_id}_service import router as {service_id}_router"
        if import_line not in content:
            content = content.replace(
                "router = APIRouter()",
                f"router = APIRouter()\n\n# Import service routers\n{import_line}"
            )
            
            # Add router inclusion
            include_line = f'router.include_router({service_id}_router, prefix="/{service_id}", tags=["{service_name}"])'
            content += f"\n\n{include_line}\n"
            
            with open(endpoints_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"✅ Service '{service_id}' created successfully!")
    print(f"   - Backend service: {service_file}")
    print(f"   - Translations updated: {LOCALES_DIR}/en.json, {LOCALES_DIR}/pt.json")
    print(f"   - Frontend will automatically detect this service via /api/services endpoint")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Create a new SILA service with form schema and i18n")
    parser.add_argument("service_id", help="Service ID (e.g., birth_certificate)")
    parser.add_argument("--name", required=True, help="Service name in Portuguese")
    parser.add_argument("--name-en", required=True, help="Service name in English")
    parser.add_argument("--description", required=True, help="Service description in Portuguese")
    parser.add_argument("--description-en", required=True, help="Service description in English")
    parser.add_argument("--module", default="civil_registry", help="Module name (default: civil_registry)")
    parser.add_argument("--category", default="civil_registration", help="Service category")
    parser.add_argument("--icon", default="document-text", help="Service icon")
    parser.add_argument("--estimated-time", default="3-5 business days", help="Estimated processing time")
    parser.add_argument("--fee", default="Free", help="Service fee")
    parser.add_argument("--config", help="JSON file with service configuration")
    
    args = parser.parse_args()
    
    # Load configuration from file or create default
    if args.config and Path(args.config).exists():
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
            fields = config.get('fields', {})
    else:
        # Default fields for a basic service
        fields = {
            "applicant_name": {
                "type": "string",
                "field_class": "str",
                "required": True,
                "label": "Nome do Requerente",
                "label_en": "Applicant Name",
                "placeholder": "Digite o nome completo"
            },
            "identity_number": {
                "type": "string", 
                "field_class": "str",
                "required": True,
                "label": "Número de Identidade",
                "label_en": "Identity Number",
                "placeholder": "Digite o número do BI"
            },
            "contact_email": {
                "type": "email",
                "field_class": "str",
                "required": False,
                "label": "Email de Contacto",
                "label_en": "Contact Email",
                "placeholder": "exemplo@email.com"
            }
        }
    
    # Create the service
    create_service(
        service_id=args.service_id,
        service_name=args.name,
        service_name_en=args.name_en,
        description=args.description,
        description_en=args.description_en,
        module_name=args.module,
        category=args.category,
        fields=fields,
        icon=args.icon,
        estimated_time=args.estimated_time,
        fee=args.fee
    )

if __name__ == "__main__":
    main()