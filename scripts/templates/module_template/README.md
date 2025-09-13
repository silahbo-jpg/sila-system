# Module Template

This template provides a standardized structure for creating new modules in the SILA-System.

## Structure

```
{module_name}/
├── __init__.py
├── models.py          # Pydantic models
├── schemas.py         # API schemas
├── crud.py           # Database operations
├── router.py         # FastAPI routes
├── services.py       # Business logic
├── dependencies.py   # Route dependencies
├── exceptions.py     # Custom exceptions
└── tests/
    ├── __init__.py
    ├── test_crud.py
    ├── test_router.py
    └── test_services.py
```

## Usage

1. Copy this template directory to `backend/app/modules/{module_name}`
2. Rename all files and update imports
3. Implement your specific business logic
4. Add routes to main router
5. Write comprehensive tests

## Standards

- Follow FastAPI best practices
- Use Pydantic for data validation
- Implement proper error handling
- Write unit tests for all functions
- Document all public APIs