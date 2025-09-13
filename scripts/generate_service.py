#!/usr/bin/env python3
# scripts/generate_service.py
# Gera um novo serviço no módulo especificado
import os
import sys
from pathlib import Path

def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"[OK] Criado diretório: {path}")

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"[OK] Criado arquivo: {path}")

# Templates básicos
TEMPLATE_MODEL = '''
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class {model_name}(Base):
    __tablename__ = "{table_name}"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(String(500))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    municipe_id = Column(Integer, nullable=False)  # Relaciona com registry
'''

TEMPLATE_SCHEMA = '''
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class {model_name}Create(BaseModel):
    nome: str
    descricao: Optional[str] = None

class {model_name}Update(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

class {model_name}Read(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    ativo: bool
    data_criacao: datetime

    class Config:
        from_attributes = True
'''

TEMPLATE_ROUTE = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.{module_name}.models.{service_slug} import {model_name}
from app.modules.{module_name}.schemas.{service_slug} import {model_name}Create, {model_name}Read, {model_name}Update
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/{api_slug}", tags=["{display_name}"])

@router.post("/", response_model={model_name}Read)
def criar_{service_slug}(data: {model_name}Create, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    db_item = {model_name}(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model={model_name}Read)
def obter_{service_slug}(item_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name} não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=list[{model_name}Read])
def listar_{service_slug}(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    return db.query({model_name}).filter({model_name}.municipe_id == current_user.id).offset(skip).limit(limit).all()

@router.put("/{item_id}", response_model={model_name}Read)
def atualizar_{service_slug}(item_id: int, data: {model_name}Update, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="{display_name} não encontrado")
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

TEMPLATE_SERVICE_REGISTRATION = '''
@register_service(
    slug="{service_slug}",
    nome="{display_name}",
    descricao="Serviço para {display_name_lower}",
    departamento="{module_name}",
    categoria="{module_name}"
)
def {service_slug}_handler(data):
    # Implementação do serviço
    return {{"status": "success"}}
'''

def main():
    if len(sys.argv) != 3:
        print("Uso: python generate_service.py <modulo> <nome_servico>")
        print("Exemplo: python generate_service.py saude AgendamentoTeleconsulta")
        sys.exit(1)

    module_name = sys.argv[1].lower()
    service_name = sys.argv[2]  # Ex: AgendamentoTeleconsulta

    # Gerar nomes
    model_name = service_name
    service_slug = ''.join(['_'+c.lower() if c.isupper() else c for c in service_name]).lstrip('_')
    api_slug = service_slug.replace('_', '-')
    table_name = f"{module_name}_{service_slug}"
    display_name = " ".join([w.capitalize() for w in service_slug.replace('_', ' ').split()])
    display_name_lower = display_name.lower()

    # Caminhos
    base_dir = Path(__file__).resolve().parent.parent
    module_path = base_dir / "backend" / "app" / "modules" / module_name
    
    if not os.path.exists(module_path):
        print(f"❌ Módulo '{module_name}' não encontrado em {module_path}")
        sys.exit(1)

    # Criar diretórios se não existirem
    models_dir = module_path / "models"
    schemas_dir = module_path / "schemas"
    routes_dir = module_path / "routes"
    
    create_directory(models_dir)
    create_directory(schemas_dir)
    create_directory(routes_dir)

    # Caminhos dos arquivos
    models_path = models_dir / f"{service_slug}.py"
    schemas_path = schemas_dir / f"{service_slug}.py"
    routes_path = routes_dir / f"{service_slug}.py"

    # Criar arquivos
    create_file(models_path, TEMPLATE_MODEL.format(model_name=model_name, table_name=table_name))
    create_file(schemas_path, TEMPLATE_SCHEMA.format(model_name=model_name))
    create_file(routes_path, TEMPLATE_ROUTE.format(
        module_name=module_name,
        service_slug=service_slug,
        api_slug=api_slug,
        model_name=model_name,
        display_name=display_name,
        item_id="id"
    ))

    # Registrar no services.py do módulo
    services_path = module_path / "services.py"
    if os.path.exists(services_path):
        # Verificar se o import do register_service já existe
        with open(services_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "from app.modules.service_hub.services import register_service" not in content:
            # Adicionar import se não existir
            import_line = "from app.modules.service_hub.services import register_service\n"
            with open(services_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Encontrar a última linha de import
            last_import_line = 0
            for i, line in enumerate(lines):
                if line.startswith("from ") or line.startswith("import "):
                    last_import_line = i
            
            # Inserir o import após a última linha de import
            lines.insert(last_import_line + 1, import_line)
            
            with open(services_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        
        # Adicionar o registro do serviço ao final do arquivo
        with open(services_path, 'a', encoding='utf-8') as f:
            f.write("\n\n" + TEMPLATE_SERVICE_REGISTRATION.format(
                service_slug=service_slug,
                display_name=display_name,
                display_name_lower=display_name_lower,
                module_name=module_name
            ))
        print(f"[OK] Serviço '{display_name}' registrado em {services_path}")

    # Registrar no __init__.py do módulo
    init_path = module_path / "__init__.py"
    if os.path.exists(init_path):
        with open(init_path, 'a', encoding='utf-8') as f:
            f.write(f"\n# Serviço: {display_name}\n")
        print(f"[OK] Serviço '{display_name}' registrado em {init_path}")

    # Registrar a rota no router do módulo
    with open(init_path, 'r', encoding='utf-8') as f:
        init_content = f.read()
    
    if "router = APIRouter()" in init_content:
        # Adicionar import da rota
        route_import = f"from app.modules.{module_name}.routes.{service_slug} import router as {service_slug}_router\n"
        route_include = f"router.include_router({service_slug}_router)\n"
        
        with open(init_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Encontrar a linha do router
        router_line = 0
        for i, line in enumerate(lines):
            if "router = APIRouter()" in line:
                router_line = i
                break
        
        # Inserir o import antes do router
        lines.insert(router_line, route_import)
        # Inserir o include_router após o router
        lines.insert(router_line + 2, route_include)
        
        with open(init_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"[OK] Rota para '{display_name}' adicionada ao router do módulo")

    print(f"\n[SUCESSO] Serviço '{display_name}' gerado com sucesso no módulo '{module_name}'!")
    print(f"[INFO] Acesse via: GET/POST em /api/{api_slug}/")

if __name__ == "__main__":
    main()
