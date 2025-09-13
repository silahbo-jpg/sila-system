from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.bolsa_familia import BolsaFamilia
from app.modules.social.schemas.bolsa_familia import BolsaFamiliaCreate, BolsaFamiliaRead, BolsaFamiliaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/bolsa-familia", tags=["Bolsa Família Municipal"])

@router.post("/", response_model=BolsaFamiliaRead)
def criar_bolsa_familia(
    data: BolsaFamiliaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Municipal Family Grant / Criar novo Bolsa Família Municipal"""
    db_item = BolsaFamilia(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=BolsaFamiliaRead)
def obter_bolsa_familia(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Municipal Family Grant by ID / Obter Bolsa Família Municipal por ID"""
    item = db.query(BolsaFamilia).filter(BolsaFamilia.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bolsa Família Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[BolsaFamiliaRead])
def listar_bolsa_familia(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Municipal Family Grant / Listar Bolsa Família Municipal"""
    return db.query(BolsaFamilia).filter(
        BolsaFamilia.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=BolsaFamiliaRead)
def atualizar_bolsa_familia(
    item_id: int, 
    data: BolsaFamiliaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Municipal Family Grant / Atualizar Bolsa Família Municipal"""
    item = db.query(BolsaFamilia).filter(BolsaFamilia.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bolsa Família Municipal não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
