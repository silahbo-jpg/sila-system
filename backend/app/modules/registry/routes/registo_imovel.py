from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.registo_imovel import RegistoImovel
from app.modules.registry.schemas.registo_imovel import RegistoImovelCreate, RegistoImovelRead, RegistoImovelUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/registo-imovel", tags=["Registo de Imóvel"])

@router.post("/", response_model=RegistoImovelRead)
def criar_registo_imovel(
    data: RegistoImovelCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Property Registration / Criar novo Registo de Imóvel"""
    db_item = RegistoImovel(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegistoImovelRead)
def obter_registo_imovel(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Property Registration by ID / Obter Registo de Imóvel por ID"""
    item = db.query(RegistoImovel).filter(RegistoImovel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Imóvel não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegistoImovelRead])
def listar_registo_imovel(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Property Registration / Listar Registo de Imóvel"""
    return db.query(RegistoImovel).filter(
        RegistoImovel.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegistoImovelRead)
def atualizar_registo_imovel(
    item_id: int, 
    data: RegistoImovelUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Property Registration / Atualizar Registo de Imóvel"""
    item = db.query(RegistoImovel).filter(RegistoImovel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registo de Imóvel não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
