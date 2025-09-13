from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.governance.models.politica_seguranca import PoliticaSeguranca
from app.modules.governance.schemas.politica_seguranca import PoliticaSegurancaCreate, PoliticaSegurancaRead, PoliticaSegurancaUpdate

router = APIRouter(prefix="/internal/politica-seguranca", tags=["Política de Segurança"])

@router.post("/", response_model=PoliticaSegurancaRead)
def criar_politica_seguranca(data: PoliticaSegurancaCreate):
    """Create new Security Policy / Criar novo Política de Segurança"""
    db_item = PoliticaSeguranca(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=PoliticaSegurancaRead)
def obter_politica_seguranca(item_id: int):
    """Get Security Policy by ID / Obter Política de Segurança por ID"""
    item = db.query(PoliticaSeguranca).filter(PoliticaSeguranca.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Política de Segurança não encontrado")
    return item

@router.get("/", response_model=List[PoliticaSegurancaRead])
def listar_politica_seguranca(skip: int = 0, limit: int = 100):
    """List Security Policy / Listar Política de Segurança"""
    return db.query(PoliticaSeguranca).offset(skip).limit(limit).all()

@router.put("/id", response_model=PoliticaSegurancaRead)
def atualizar_politica_seguranca(item_id: int, data: PoliticaSegurancaUpdate):
    """Update Security Policy / Atualizar Política de Segurança"""
    item = db.query(PoliticaSeguranca).filter(PoliticaSeguranca.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Política de Segurança não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
