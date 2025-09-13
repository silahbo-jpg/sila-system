from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.cartao_vacina import CartaoVacina
from app.modules.health.schemas.cartao_vacina import CartaoVacinaCreate, CartaoVacinaRead, CartaoVacinaUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/cartao-vacina", tags=["Cartão de Vacinação Digital"])

@router.post("/", response_model=CartaoVacinaRead)
def criar_cartao_vacina(
    data: CartaoVacinaCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Digital Vaccination Card / Criar novo Cartão de Vacinação Digital"""
    db_item = CartaoVacina(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=CartaoVacinaRead)
def obter_cartao_vacina(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Digital Vaccination Card by ID / Obter Cartão de Vacinação Digital por ID"""
    item = db.query(CartaoVacina).filter(CartaoVacina.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cartão de Vacinação Digital não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[CartaoVacinaRead])
def listar_cartao_vacina(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Digital Vaccination Card / Listar Cartão de Vacinação Digital"""
    return db.query(CartaoVacina).filter(
        CartaoVacina.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=CartaoVacinaRead)
def atualizar_cartao_vacina(
    item_id: int, 
    data: CartaoVacinaUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Digital Vaccination Card / Atualizar Cartão de Vacinação Digital"""
    item = db.query(CartaoVacina).filter(CartaoVacina.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cartão de Vacinação Digital não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
