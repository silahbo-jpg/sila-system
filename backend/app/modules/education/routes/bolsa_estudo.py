from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.education.models.bolsa_estudo import BolsaEstudo
from app.modules.education.schemas.bolsa_estudo import BolsaEstudoCreate, BolsaEstudoRead, BolsaEstudoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/bolsa-estudo", tags=["Bolsa de Estudo Municipal"])

@router.post("/", response_model=BolsaEstudoRead)
def criar_bolsa_estudo(
    data: BolsaEstudoCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Municipal Study Grant / Criar novo Bolsa de Estudo Municipal"""
    db_item = BolsaEstudo(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=BolsaEstudoRead)
def obter_bolsa_estudo(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Municipal Study Grant by ID / Obter Bolsa de Estudo Municipal por ID"""
    item = db.query(BolsaEstudo).filter(BolsaEstudo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bolsa de Estudo Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[BolsaEstudoRead])
def listar_bolsa_estudo(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Municipal Study Grant / Listar Bolsa de Estudo Municipal"""
    return db.query(BolsaEstudo).filter(
        BolsaEstudo.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=BolsaEstudoRead)
def atualizar_bolsa_estudo(
    item_id: int, 
    data: BolsaEstudoUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Municipal Study Grant / Atualizar Bolsa de Estudo Municipal"""
    item = db.query(BolsaEstudo).filter(BolsaEstudo.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bolsa de Estudo Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
