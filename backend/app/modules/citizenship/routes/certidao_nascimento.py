from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.certidao_nascimento import CertidaoNascimento
from app.modules.citizenship.schemas.certidao_nascimento import CertidaoNascimentoCreate, CertidaoNascimentoRead, CertidaoNascimentoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/certidao-nascimento", tags=["Certidão de Nascimento"])

@router.post("/", response_model=CertidaoNascimentoRead)
def criar_certidao_nascimento(
    data: CertidaoNascimentoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Birth Certificate / Criar novo Certidão de Nascimento"""
    db_item = CertidaoNascimento(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CertidaoNascimentoRead)
def obter_certidao_nascimento(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Birth Certificate by ID / Obter Certidão de Nascimento por ID"""
    item = db.query(CertidaoNascimento).filter(CertidaoNascimento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão de Nascimento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CertidaoNascimentoRead])
def listar_certidao_nascimento(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Birth Certificate / Listar Certidão de Nascimento"""
    return db.query(CertidaoNascimento).filter(
        CertidaoNascimento.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CertidaoNascimentoRead)
def atualizar_certidao_nascimento(
    item_id: int, 
    data: CertidaoNascimentoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Birth Certificate / Atualizar Certidão de Nascimento"""
    item = db.query(CertidaoNascimento).filter(CertidaoNascimento.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Certidão de Nascimento não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
