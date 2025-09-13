from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.address.models.validacao_c_e_p import ValidacaoCEP
from app.modules.address.schemas.validacao_c_e_p import ValidacaoCEPCreate, ValidacaoCEPRead, ValidacaoCEPUpdate

router = APIRouter(prefix="/internal/validacao-c-e-p", tags=["Validação de CEP"])

@router.post("/", response_model=ValidacaoCEPRead)
def criar_validacao_c_e_p(data: ValidacaoCEPCreate):
    """Create new ZIP Code Validation / Criar novo Validação de CEP"""
    db_item = ValidacaoCEP(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ValidacaoCEPRead)
def obter_validacao_c_e_p(item_id: int):
    """Get ZIP Code Validation by ID / Obter Validação de CEP por ID"""
    item = db.query(ValidacaoCEP).filter(ValidacaoCEP.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Validação de CEP não encontrado")
    return item

@router.get("/", response_model=List[ValidacaoCEPRead])
def listar_validacao_c_e_p(skip: int = 0, limit: int = 100):
    """List ZIP Code Validation / Listar Validação de CEP"""
    return db.query(ValidacaoCEP).offset(skip).limit(limit).all()

@router.put("/id", response_model=ValidacaoCEPRead)
def atualizar_validacao_c_e_p(item_id: int, data: ValidacaoCEPUpdate):
    """Update ZIP Code Validation / Atualizar Validação de CEP"""
    item = db.query(ValidacaoCEP).filter(ValidacaoCEP.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Validação de CEP não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
