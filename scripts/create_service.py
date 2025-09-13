#!/usr/bin/env python3
# scripts/create_service.py
# Enhanced service generation script with CSV support and bilingual names
import os
import sys
import csv
import argparse
from pathlib import Path

def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"[OK] Criado diretório: {path}")

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"[OK] Criado arquivo: {path}")

# Enhanced templates with bilingual support
TEMPLATE_MODEL = '''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class {model_name}(Base):
    __tablename__ = "{table_name}"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    nome_en = Column(String(200), nullable=False)  # English name
    descricao = Column(String(500))
    descricao_en = Column(String(500))  # English description
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    dados_adicionais = Column(JSON)  # For flexible additional data
    # Conditional relationship based on service type
    municipe_id = Column(Integer, nullable={nullable_municipe})  # Only for citizen services
    status = Column(String(50), default="pendente")
'''

TEMPLATE_SCHEMA = '''
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class {model_name}Create(BaseModel):
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None

class {model_name}Update(BaseModel):
    nome: Optional[str] = None
    nome_en: Optional[str] = None
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: Optional[bool] = None
    status: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None

class {model_name}Read(BaseModel):
    id: int
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    status: str
    dados_adicionais: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
'''

TEMPLATE_ROUTE_CITIZEN = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.{module_name}.models.{service_slug} import {model_name}
from app.modules.{module_name}.schemas.{service_slug} import {model_name}Create, {model_name}Read, {model_name}Update
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/{api_slug}", tags=["{display_name_pt}"])

@router.post("/", response_model={model_name}Read)
def criar_{service_slug}(
    data: {model_name}Create, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    """Create new {display_name_en} / Criar novo {display_name_pt}"""
    db_item = {model_name}(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model={model_name}Read)
def obter_{service_slug}(
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    """Get {display_name_en} by ID / Obter {display_name_pt} por ID"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[{model_name}Read])
def listar_{service_slug}(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    """List {display_name_en} / Listar {display_name_pt}"""
    return db.query({model_name}).filter(
        {model_name}.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/{item_id}", response_model={model_name}Read)
def atualizar_{service_slug}(
    item_id: int, 
    data: {model_name}Update, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    """Update {display_name_en} / Atualizar {display_name_pt}"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
'''

TEMPLATE_ROUTE_INTERNAL = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.{module_name}.models.{service_slug} import {model_name}
from app.modules.{module_name}.schemas.{service_slug} import {model_name}Create, {model_name}Read, {model_name}Update

router = APIRouter(prefix="/internal/{api_slug}", tags=["{display_name_pt}"])

@router.post("/", response_model={model_name}Read)
def criar_{service_slug}(data: {model_name}Create, db: Session = Depends(get_db)):
    """Create new {display_name_en} / Criar novo {display_name_pt}"""
    db_item = {model_name}(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model={model_name}Read)
def obter_{service_slug}(item_id: int, db: Session = Depends(get_db)):
    """Get {display_name_en} by ID / Obter {display_name_pt} por ID"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    return item

@router.get("/", response_model=List[{model_name}Read])
def listar_{service_slug}(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List {display_name_en} / Listar {display_name_pt}"""
    return db.query({model_name}).offset(skip).limit(limit).all()

@router.put("/{item_id}", response_model={model_name}Read)
def atualizar_{service_slug}(item_id: int, data: {model_name}Update, db: Session = Depends(get_db)):
    """Update {display_name_en} / Atualizar {display_name_pt}"""
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name_pt} não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
'''

TEMPLATE_SERVICE_REGISTRATION = '''
@register_service(
    slug="{service_slug}",
    nome="{display_name_pt}",
    nome_en="{display_name_en}",
    descricao="Serviço para {display_name_pt_lower}",
    descricao_en="Service for {display_name_en_lower}",
    departamento="{module_name}",
    categoria="{module_name}",
    tipo_servico="{service_type}"
)
def {service_slug}_handler(data):
    """
    Handler for {display_name_en} / Manipulador para {display_name_pt}
    """
    return {{"status": "success", "service": "{service_slug}"}}
'''

def generate_service(module_name, service_key, service_name_pt, service_name_en, service_type="citizen"):
    """Generate a single service with bilingual support"""
    
    # Generate names and slugs
    model_name = service_key
    service_slug = ''.join(['_'+c.lower() if c.isupper() else c for c in service_key]).lstrip('_')
    api_slug = service_slug.replace('_', '-')
    table_name = f"{module_name}_{service_slug}"
    
    display_name_pt = service_name_pt
    display_name_en = service_name_en
    display_name_pt_lower = display_name_pt.lower()
    display_name_en_lower = display_name_en.lower()
    
    # Determine if municipe_id should be nullable
    nullable_municipe = "True" if service_type == "internal" else "False"
    
    # Paths
    base_dir = Path(__file__).resolve().parent.parent
    module_path = base_dir / "backend" / "app" / "modules" / module_name
    
    if not os.path.exists(module_path):
        print(f"❌ Módulo '{module_name}' não encontrado em {module_path}")
        return False

    # Create directories if they don't exist
    models_dir = module_path / "models"
    schemas_dir = module_path / "schemas"
    routes_dir = module_path / "routes"
    
    create_directory(models_dir)
    create_directory(schemas_dir)
    create_directory(routes_dir)

    # File paths
    models_path = models_dir / f"{service_slug}.py"
    schemas_path = schemas_dir / f"{service_slug}.py"
    routes_path = routes_dir / f"{service_slug}.py"

    # Create files
    create_file(models_path, TEMPLATE_MODEL.format(
        model_name=model_name,
        table_name=table_name,
        nullable_municipe=nullable_municipe
    ))
    
    create_file(schemas_path, TEMPLATE_SCHEMA.format(model_name=model_name))
    
    # Choose route template based on service type
    route_template = TEMPLATE_ROUTE_CITIZEN if service_type == "citizen" else TEMPLATE_ROUTE_INTERNAL
    
    create_file(routes_path, route_template.format(
        module_name=module_name,
        service_slug=service_slug,
        api_slug=api_slug,
        model_name=model_name,
        display_name_pt=display_name_pt,
        display_name_en=display_name_en,
        item_id="id"
    ))

    # Register in services.py
    services_path = module_path / "services.py"
    if os.path.exists(services_path):
        # Check if register_service import exists
        with open(services_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "from app.modules.service_hub.services import register_service" not in content:
            # Add import if it doesn't exist
            import_line = "from app.modules.service_hub.services import register_service\n"
            with open(services_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find last import line
            last_import_line = 0
            for i, line in enumerate(lines):
                if line.startswith("from ") or line.startswith("import "):
                    last_import_line = i
            
            # Insert import after last import line
            lines.insert(last_import_line + 1, import_line)
            
            with open(services_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        
        # Add service registration to end of file
        with open(services_path, 'a', encoding='utf-8') as f:
            f.write("\n\n" + TEMPLATE_SERVICE_REGISTRATION.format(
                service_slug=service_slug,
                display_name_pt=display_name_pt,
                display_name_en=display_name_en,
                display_name_pt_lower=display_name_pt_lower,
                display_name_en_lower=display_name_en_lower,
                module_name=module_name,
                service_type=service_type
            ))
        print(f"[OK] Serviço '{display_name_pt}' registrado em {services_path}")

    # Register in module __init__.py
    init_path = module_path / "__init__.py"
    if os.path.exists(init_path):
        with open(init_path, 'a', encoding='utf-8') as f:
            f.write(f"\n# Serviço: {display_name_pt} / {display_name_en}\n")
        print(f"[OK] Serviço '{display_name_pt}' registrado em {init_path}")

    # Register route in module router
    with open(init_path, 'r', encoding='utf-8') as f:
        init_content = f.read()
    
    if "router = APIRouter()" in init_content:
        # Add route import and include
        route_import = f"from app.modules.{module_name}.routes.{service_slug} import router as {service_slug}_router\n"
        route_include = f"router.include_router({service_slug}_router)\n"
        
        with open(init_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find router line
        router_line = 0
        for i, line in enumerate(lines):
            if "router = APIRouter()" in line:
                router_line = i
                break
        
        # Insert import before router
        lines.insert(router_line, route_import)
        # Insert include_router after router
        lines.insert(router_line + 2, route_include)
        
        with open(init_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"[OK] Rota para '{display_name_pt}' adicionada ao router do módulo")

    print(f"\n[SUCESSO] Serviço '{display_name_pt}' / '{display_name_en}' gerado com sucesso!")
    return True

def generate_from_csv(csv_file):
    """Generate services from CSV file"""
    services_created = 0
    services_failed = 0
    failed_services = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            services = list(reader)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo CSV: {str(e)}")
        return
    
    print(f"[INICIO] Iniciando geração de {len(services)} serviços do arquivo CSV...\n")
    
    for i, service in enumerate(services, 1):
        # Skip comment lines
        if service['module'].startswith('#'):
            continue
            
        module = service['module'].strip()
        service_key = service['service_key'].strip()
        service_name_pt = service['service_name_pt'].strip()
        service_name_en = service['service_name_en'].strip()
        service_type = service.get('service_type', 'citizen').strip()
        
        print(f"[{i}/{len(services)}] Gerando {service_name_pt} ({service_name_en}) no módulo {module}...")
        
        if generate_service(module, service_key, service_name_pt, service_name_en, service_type):
            services_created += 1
            print(f"[OK] {service_name_pt} gerado com sucesso!")
        else:
            services_failed += 1
            failed_services.append((module, service_key, service_name_pt, service_name_en))
            print(f"[ERRO] Falha ao gerar {service_name_pt}")
        
        print("-" * 50)
    
    # Summary
    print(f"\n[RESUMO]")
    print(f"✅ Serviços criados com sucesso: {services_created}")
    print(f"❌ Serviços falharam: {services_failed}")
    
    if failed_services:
        print(f"\n[FALHAS]")
        for module, service_key, name_pt, name_en in failed_services:
            print(f"  - {module}/{service_key}: {name_pt} ({name_en})")

def main():
    parser = argparse.ArgumentParser(description="Enhanced Service Generator with CSV support and bilingual names")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", type=str, help="Path to CSV file with services to generate")
    group.add_argument("--single", nargs=4, metavar=('MODULE', 'SERVICE_KEY', 'NAME_PT', 'NAME_EN'), 
                      help="Generate single service: module service_key name_pt name_en")
    
    parser.add_argument("--type", choices=['citizen', 'internal'], default='citizen',
                       help="Service type (default: citizen)")
    
    args = parser.parse_args()
    
    if args.input:
        generate_from_csv(args.input)
    elif args.single:
        module, service_key, name_pt, name_en = args.single
        success = generate_service(module, service_key, name_pt, name_en, args.type)
        if success:
            print(f"\n[SUCESSO] Serviço gerado com sucesso!")
        else:
            print(f"\n[ERRO] Falha ao gerar serviço!")
            sys.exit(1)

if __name__ == "__main__":
    main()