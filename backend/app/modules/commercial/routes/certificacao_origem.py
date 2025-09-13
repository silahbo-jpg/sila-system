from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.commercial.models.certificacao_origem import CertificacaoOrigem
from app.modules.commercial.schemas.certificacao_origem import CertificacaoOrigemCreate, CertificacaoOrigemRead, CertificacaoOrigemUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/certificacao-origem", tags=["Certificação de Origem"])

@router.post("/", response_model=CertificacaoOrigemRead)
def criar_certificacao_origem(
    data: CertificacaoOrigemCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Origin Certification / Criar novo Certificação de Origem"""
    db_item = CertificacaoOrigem(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CertificacaoOrigemRead)
def obter_certificacao_origem(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Origin Certification by ID / Obter Certificação de Origem por ID"""
    item = db.query(CertificacaoOrigem).filter(CertificacaoOrigem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certificação de Origem não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CertificacaoOrigemRead])
def listar_certificacao_origem(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Origin Certification / Listar Certificação de Origem"""
    return db.query(CertificacaoOrigem).filter(
        CertificacaoOrigem.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CertificacaoOrigemRead)
def atualizar_certificacao_origem(
    item_id: int, 
    data: CertificacaoOrigemUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Origin Certification / Atualizar Certificação de Origem"""
    item = db.query(CertificacaoOrigem).filter(CertificacaoOrigem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certificação de Origem não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
