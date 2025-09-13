from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.certidao_negativa import CertidaoNegativa
from app.modules.registry.schemas.certidao_negativa import CertidaoNegativaCreate, CertidaoNegativaRead, CertidaoNegativaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/certidao-negativa", tags=["Certidão Negativa"])

@router.post("/", response_model=CertidaoNegativaRead)
def criar_certidao_negativa(
    data: CertidaoNegativaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Negative Certificate / Criar novo Certidão Negativa"""
    db_item = CertidaoNegativa(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CertidaoNegativaRead)
def obter_certidao_negativa(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Negative Certificate by ID / Obter Certidão Negativa por ID"""
    item = db.query(CertidaoNegativa).filter(CertidaoNegativa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão Negativa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CertidaoNegativaRead])
def listar_certidao_negativa(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Negative Certificate / Listar Certidão Negativa"""
    return db.query(CertidaoNegativa).filter(
        CertidaoNegativa.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CertidaoNegativaRead)
def atualizar_certidao_negativa(
    item_id: int, 
    data: CertidaoNegativaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Negative Certificate / Atualizar Certidão Negativa"""
    item = db.query(CertidaoNegativa).filter(CertidaoNegativa.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão Negativa não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
