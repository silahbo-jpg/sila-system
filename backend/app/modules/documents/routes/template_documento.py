from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.documents.models.template_documento import TemplateDocumento
from app.modules.documents.schemas.template_documento import TemplateDocumentoCreate, TemplateDocumentoRead, TemplateDocumentoUpdate

router = APIRouter(prefix="/internal/template-documento", tags=["Template de Documento"])

@router.post("/", response_model=TemplateDocumentoRead)
def criar_template_documento(data: TemplateDocumentoCreate):
    """Create new Document Template / Criar novo Template de Documento"""
    db_item = TemplateDocumento(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=TemplateDocumentoRead)
def obter_template_documento(item_id: int):
    """Get Document Template by ID / Obter Template de Documento por ID"""
    item = db.query(TemplateDocumento).filter(TemplateDocumento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Template de Documento não encontrado")
    return item

@router.get("/", response_model=List[TemplateDocumentoRead])
def listar_template_documento(skip: int = 0, limit: int = 100):
    """List Document Template / Listar Template de Documento"""
    return db.query(TemplateDocumento).offset(skip).limit(limit).all()

@router.put("/id", response_model=TemplateDocumentoRead)
def atualizar_template_documento(item_id: int, data: TemplateDocumentoUpdate):
    """Update Document Template / Atualizar Template de Documento"""
    item = db.query(TemplateDocumento).filter(TemplateDocumento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Template de Documento não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
