#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para adicionar um novo serviço ao sila_dev

Este script facilita a criação de novos serviços no sistema sila_dev,
gerando a estrutura básica de arquivos e código necessários.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / "backend" / "app" / "modules"

# Template para o arquivo __init__.py
INIT_TEMPLATE = '''
# {module_name} Module
# Sistema Integrado Local de sila_dev-systemistração (sila_dev)

"""
Módulo {module_title}

Este módulo é responsável por {module_description}
"""

from fastapi import APIRouter

router = APIRouter()
'''

# Template para o arquivo models.py
MODELS_TEMPLATE = '''
# {module_name} Models
# Sistema Integrado Local de sila_dev-systemistração (sila_dev)

"""
Modelos de dados para o módulo {module_title}.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

# Defina seus modelos aqui
'''

# Template para o arquivo schemas.py
SCHEMAS_TEMPLATE = '''
# {module_name} Schemas
# Sistema Integrado Local de sila_dev-systemistração (sila_dev)

"""
Esquemas de validação para o módulo {module_title}.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# Defina seus esquemas aqui
'''

# Template para o arquivo crud.py
CRUD_TEMPLATE = '''
# {module_name} CRUD Operations
# Sistema Integrado Local de sila_dev-systemistração (sila_dev)

"""
Operações CRUD para o módulo {module_title}.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from . import models, schemas

# Implemente suas operações CRUD aqui
'''

# Template para o arquivo services.py
SERVICES_TEMPLATE = '''
# {module_name} Services
# Sistema Integrado Local de sila_dev-systemistração (sila_dev)

"""
Serviços de negócio para o módulo {module_title}.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.modules.service_hub.services import register_service
from . import crud, models, schemas

# Exemplo de uso do decorator register_service
# @register_service(
#     slug="{module_slug}-exemplo",
#     nome="Serviço de Exemplo",
#     descricao="Descrição do serviço de exemplo",
#     departamento="{module_slug}",
#     categoria="geral"
# )
# def exemplo_handler(data):
#     # Implementação do serviço
#     return {"status": "success"}

# Implemente seus serviços aqui
'''

# Template para o arquivo endpoints.py
ENDPOINTS_TEMPLATE = '''
# {module_name} Endpoints
# Sistema Integrado Local de sila_dev-systemistração (sila_dev)

"""
Endpoints da API para o módulo {module_title}.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth_utils import get_current_active_user
from . import crud, schemas, models, services

router = APIRouter()

# Implemente seus endpoints aqui
'''

# Template para o arquivo README.md
README_TEMPLATE = '''
# Módulo {module_title}

## Descrição
{module_description}

## Funcionalidades
- Funcionalidade 1
- Funcionalidade 2

## Estrutura
- `models.py`: Modelos de dados
- `schemas.py`: Esquemas de validação
- `crud.py`: Operações CRUD
- `services.py`: Serviços de negócio
- `endpoints.py`: Endpoints da API

## Como usar
```python
# Exemplo de uso
```
'''


def create_module_structure(module_name, module_title, module_description):
    """Cria a estrutura básica de um novo módulo."""
    module_slug = module_name.lower()
    module_dir = MODULES_DIR / module_slug
    
    # Verifica se o módulo já existe
    if module_dir.exists():
        print(f"O módulo '{module_slug}' já existe!")
        return False
    
    # Cria o diretório do módulo
    module_dir.mkdir(exist_ok=True)
    
    # Cria os subdiretórios
    (module_dir / "models").mkdir(exist_ok=True)
    (module_dir / "routes").mkdir(exist_ok=True)
    (module_dir / "services").mkdir(exist_ok=True)
    (module_dir / "tests").mkdir(exist_ok=True)
    
    # Cria os arquivos básicos
    with open(module_dir / "__init__.py", "w", encoding="utf-8") as f:
        f.write(INIT_TEMPLATE.format(
            module_name=module_name,
            module_title=module_title,
            module_description=module_description
        ))
    
    with open(module_dir / "models.py", "w", encoding="utf-8") as f:
        f.write(MODELS_TEMPLATE.format(
            module_name=module_name,
            module_title=module_title
        ))
    
    with open(module_dir / "schemas.py", "w", encoding="utf-8") as f:
        f.write(SCHEMAS_TEMPLATE.format(
            module_name=module_name,
            module_title=module_title
        ))
    
    with open(module_dir / "crud.py", "w", encoding="utf-8") as f:
        f.write(CRUD_TEMPLATE.format(
            module_name=module_name,
            module_title=module_title
        ))
    
    with open(module_dir / "services.py", "w", encoding="utf-8") as f:
        f.write(SERVICES_TEMPLATE.format(
            module_name=module_name,
            module_title=module_title,
            module_slug=module_slug
        ))
    
    with open(module_dir / "endpoints.py", "w", encoding="utf-8") as f:
        f.write(ENDPOINTS_TEMPLATE.format(
            module_name=module_name,
            module_title=module_title
        ))
    
    with open(module_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(README_TEMPLATE.format(
            module_title=module_title,
            module_description=module_description
        ))
    
    print(f"Módulo '{module_slug}' criado com sucesso!")
    return True


def main():
    parser = argparse.ArgumentParser(description="Cria um novo módulo no sila_dev")
    parser.add_argument("module_name", help="Nome do módulo (ex: Finance)")
    parser.add_argument("--title", help="Título do módulo (ex: Finanças)")
    parser.add_argument("--description", help="Descrição do módulo")
    
    args = parser.parse_args()
    
    module_name = args.module_name
    module_title = args.title or module_name
    module_description = args.description or f"gerenciar funcionalidades relacionadas a {module_title.lower()}"
    
    create_module_structure(module_name, module_title, module_description)


if __name__ == "__main__":
    main()

