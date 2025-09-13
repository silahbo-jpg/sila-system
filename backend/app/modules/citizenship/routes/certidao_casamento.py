from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.certidao_casamento import CertidaoCasamento
from app.modules.citizenship.schemas.certidao_casamento import CertidaoCasamentoCreate, CertidaoCasamentoRead, CertidaoCasamentoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/certidao-casamento", tags=["Certidão de Casamento"])

@router.post("/", response_model=CertidaoCasamentoRead)
def criar_certidao_casamento(
    data: CertidaoCasamentoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Marriage Certificate / Criar novo Certidão de Casamento"""
    db_item = CertidaoCasamento(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CertidaoCasamentoRead)
def obter_certidao_casamento(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Marriage Certificate by ID / Obter Certidão de Casamento por ID"""
    item = db.query(CertidaoCasamento).filter(CertidaoCasamento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão de Casamento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CertidaoCasamentoRead])
def listar_certidao_casamento(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Marriage Certificate / Listar Certidão de Casamento"""
    return db.query(CertidaoCasamento).filter(
        CertidaoCasamento.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CertidaoCasamentoRead)
def atualizar_certidao_casamento(
    item_id: int, 
    data: CertidaoCasamentoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Marriage Certificate / Atualizar Certidão de Casamento"""
    item = db.query(CertidaoCasamento).filter(CertidaoCasamento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão de Casamento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
