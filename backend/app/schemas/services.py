"""
Service Models and Schemas for Dynamic Service Loading

This module defines the data structures for the dynamic service system
that enables automatic frontend-backend synchronization.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ServiceStatus(str, Enum):
    """Service status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"


class UserRole(str, Enum):
    """User role enumeration"""
    CITIZEN = "citizen"
    STAFF = "staff"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class FieldType(str, Enum):
    """Form field type enumeration"""
    STRING = "string"
    EMAIL = "email"
    PHONE = "phone"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    SELECT = "select"
    MULTISELECT = "multiselect"
    TEXTAREA = "textarea"
    FILE = "file"
    PASSWORD = "password"


class FormField(BaseModel):
    """Form field definition"""
    name: str = Field(..., description="Field name/key")
    label: str = Field(..., description="Display label")
    type: FieldType = Field(..., description="Field input type")
    required: bool = Field(default=False, description="Whether field is required")
    placeholder: Optional[str] = Field(None, description="Placeholder text")
    help_text: Optional[str] = Field(None, description="Help text for field")
    default_value: Optional[Union[str, int, bool, List[str]]] = Field(None, description="Default value")
    options: Optional[List[Dict[str, Any]]] = Field(None, description="Options for select fields")
    validation: Optional[Dict[str, Any]] = Field(None, description="Validation rules")
    conditional: Optional[Dict[str, Any]] = Field(None, description="Conditional display rules")


class FormSchema(BaseModel):
    """Form schema definition"""
    title: str = Field(..., description="Form title")
    description: Optional[str] = Field(None, description="Form description")
    fields: List[FormField] = Field(..., description="Form fields")
    submit_button_text: Optional[str] = Field("Submit", description="Submit button text")
    cancel_button_text: Optional[str] = Field("Cancel", description="Cancel button text")
    validation_rules: Optional[Dict[str, Any]] = Field(None, description="Form-level validation")


class ServiceTranslations(BaseModel):
    """Service name and description translations"""
    en: Dict[str, str] = Field(..., description="English translations")
    pt: Dict[str, str] = Field(..., description="Portuguese translations")


class ServiceMetadata(BaseModel):
    """Additional service metadata"""
    category: Optional[str] = Field(None, description="Service category")
    estimated_time: Optional[str] = Field(None, description="Estimated processing time")
    required_documents: Optional[List[str]] = Field(None, description="Required documents")
    fee: Optional[str] = Field(None, description="Service fee")
    prerequisites: Optional[List[str]] = Field(None, description="Prerequisites")
    municipality_specific: bool = Field(False, description="Whether service is municipality-specific")
    online_only: bool = Field(False, description="Whether service is online-only")


class ServiceDefinition(BaseModel):
    """Complete service definition"""
    id: str = Field(..., description="Unique service identifier")
    name: str = Field(..., description="Service name (default language)")
    description: Optional[str] = Field(None, description="Service description")
    module: str = Field(..., description="Backend module name")
    icon: Optional[str] = Field("document", description="Icon name for UI")
    roles: List[UserRole] = Field(..., description="Roles that can access this service")
    status: ServiceStatus = Field(ServiceStatus.ACTIVE, description="Service status")
    api_endpoint: str = Field(..., description="API endpoint for service")
    form_schema: Optional[FormSchema] = Field(None, description="Form schema for service")
    translations: Optional[ServiceTranslations] = Field(None, description="Translations")
    metadata: Optional[ServiceMetadata] = Field(None, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class ServiceListResponse(BaseModel):
    """Response for service list endpoint"""
    services: List[ServiceDefinition] = Field(..., description="List of services")
    total: int = Field(..., description="Total number of services")
    filtered: int = Field(..., description="Number of services after filtering")


class ServiceCreateRequest(BaseModel):
    """Request for creating a new service"""
    id: str = Field(..., description="Unique service identifier")
    name: str = Field(..., description="Service name")
    description: Optional[str] = None
    module: str = Field(..., description="Backend module name")
    icon: Optional[str] = "document"
    roles: List[UserRole] = Field(..., description="Roles that can access this service")
    api_endpoint: str = Field(..., description="API endpoint for service")
    form_schema: Optional[FormSchema] = None
    translations: Optional[ServiceTranslations] = None
    metadata: Optional[ServiceMetadata] = None


class ServiceUpdateRequest(BaseModel):
    """Request for updating an existing service"""
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    roles: Optional[List[UserRole]] = None
    status: Optional[ServiceStatus] = None
    form_schema: Optional[FormSchema] = None
    translations: Optional[ServiceTranslations] = None
    metadata: Optional[ServiceMetadata] = None


# Default service definitions for SILA system
DEFAULT_SERVICES = [
    {
        "id": "birth_certificate",
        "name": "Birth Certificate",
        "description": "Request an official birth certificate",
        "module": "civil_registry",
        "icon": "document-text",
        "roles": ["citizen", "staff"],
        "api_endpoint": "/api/v1/civil-registry/birth-certificate",
        "metadata": {
            "category": "civil_registration",
            "estimated_time": "3-5 business days",
            "fee": "Free",
            "required_documents": ["Parent's ID", "Hospital birth record"]
        }
    },
    {
        "id": "business_license",
        "name": "Business License",
        "description": "Apply for a business operating license",
        "module": "business_registry",
        "icon": "building-office",
        "roles": ["citizen", "staff"],
        "api_endpoint": "/api/v1/business/license",
        "metadata": {
            "category": "business_licensing",
            "estimated_time": "7-10 business days",
            "fee": "15,000 Kz",
            "required_documents": ["ID Card", "Tax Number", "Business Plan"]
        }
    },
    {
        "id": "residence_change",
        "name": "Change of Residence",
        "description": "Register a change of residential address",
        "module": "citizen_registry", 
        "icon": "home",
        "roles": ["citizen", "staff"],
        "api_endpoint": "/api/v1/citizen/residence-change",
        "metadata": {
            "category": "civil_registration",
            "estimated_time": "1-2 business days",
            "fee": "2,000 Kz",
            "required_documents": ["ID Card", "Residence Proof"]
        }
    }
]