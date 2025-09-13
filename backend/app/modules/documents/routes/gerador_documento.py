from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.documents.models.gerador_documento import GeradorDocumento
from app.modules.documents.schemas.gerador_documento import GeradorDocumentoCreate, GeradorDocumentoRead, GeradorDocumentoUpdate

router = APIRouter(prefix="/internal/gerador-documento", tags=["Gerador de Documento"])

@router.post("/", response_model=GeradorDocumentoRead)
def criar_gerador_documento(data: GeradorDocumentoCreate):
    """Create new Document Generator / Criar novo Gerador de Documento"""
    db_item = GeradorDocumento(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=GeradorDocumentoRead)
def obter_gerador_documento(item_id: int):
    """Get Document Generator by ID / Obter Gerador de Documento por ID"""
    item = db.query(GeradorDocumento).filter(GeradorDocumento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gerador de Documento não encontrado")
    return item

@router.get("/", response_model=List[GeradorDocumentoRead])
def listar_gerador_documento(skip: int = 0, limit: int = 100):
    """List Document Generator / Listar Gerador de Documento"""
    return db.query(GeradorDocumento).offset(skip).limit(limit).all()

@router.put("/id", response_model=GeradorDocumentoRead)
def atualizar_gerador_documento(item_id: int, data: GeradorDocumentoUpdate):
    """Update Document Generator / Atualizar Gerador de Documento"""
    item = db.query(GeradorDocumento).filter(GeradorDocumento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gerador de Documento não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
