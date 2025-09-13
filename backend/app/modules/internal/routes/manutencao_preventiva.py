from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.internal.models.manutencao_preventiva import ManutencaoPreventiva
from app.modules.internal.schemas.manutencao_preventiva import ManutencaoPreventivaCreate, ManutencaoPreventivaRead, ManutencaoPreventivaUpdate

router = APIRouter(prefix="/internal/manutencao-preventiva", tags=["Manutenção Preventiva"])

@router.post("/", response_model=ManutencaoPreventivaRead)
def criar_manutencao_preventiva(data: ManutencaoPreventivaCreate):
    """Create new Preventive Maintenance / Criar novo Manutenção Preventiva"""
    db_item = ManutencaoPreventiva(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ManutencaoPreventivaRead)
def obter_manutencao_preventiva(item_id: int):
    """Get Preventive Maintenance by ID / Obter Manutenção Preventiva por ID"""
    item = db.query(ManutencaoPreventiva).filter(ManutencaoPreventiva.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Manutenção Preventiva não encontrado")
    return item

@router.get("/", response_model=List[ManutencaoPreventivaRead])
def listar_manutencao_preventiva(skip: int = 0, limit: int = 100):
    """List Preventive Maintenance / Listar Manutenção Preventiva"""
    return db.query(ManutencaoPreventiva).offset(skip).limit(limit).all()

@router.put("/id", response_model=ManutencaoPreventivaRead)
def atualizar_manutencao_preventiva(item_id: int, data: ManutencaoPreventivaUpdate):
    """Update Preventive Maintenance / Atualizar Manutenção Preventiva"""
    item = db.query(ManutencaoPreventiva).filter(ManutencaoPreventiva.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Manutenção Preventiva não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
