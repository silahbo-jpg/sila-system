from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.certidao_obito import CertidaoObito
from app.modules.citizenship.schemas.certidao_obito import CertidaoObitoCreate, CertidaoObitoRead, CertidaoObitoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/certidao-obito", tags=["Certidão de Óbito"])

@router.post("/", response_model=CertidaoObitoRead)
def criar_certidao_obito(
    data: CertidaoObitoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Death Certificate / Criar novo Certidão de Óbito"""
    db_item = CertidaoObito(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CertidaoObitoRead)
def obter_certidao_obito(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Death Certificate by ID / Obter Certidão de Óbito por ID"""
    item = db.query(CertidaoObito).filter(CertidaoObito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão de Óbito não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CertidaoObitoRead])
def listar_certidao_obito(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Death Certificate / Listar Certidão de Óbito"""
    return db.query(CertidaoObito).filter(
        CertidaoObito.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CertidaoObitoRead)
def atualizar_certidao_obito(
    item_id: int, 
    data: CertidaoObitoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Death Certificate / Atualizar Certidão de Óbito"""
    item = db.query(CertidaoObito).filter(CertidaoObito.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão de Óbito não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
