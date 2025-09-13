from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.health.models.avaliacao_nutricional import AvaliacaoNutricional
from app.modules.health.schemas.avaliacao_nutricional import AvaliacaoNutricionalCreate, AvaliacaoNutricionalRead, AvaliacaoNutricionalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/avaliacao-nutricional", tags=["Avaliação Nutricional"])

@router.post("/", response_model=AvaliacaoNutricionalRead)
def criar_avaliacao_nutricional(
    data: AvaliacaoNutricionalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Nutritional Assessment / Criar novo Avaliação Nutricional"""
    db_item = AvaliacaoNutricional(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AvaliacaoNutricionalRead)
def obter_avaliacao_nutricional(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Nutritional Assessment by ID / Obter Avaliação Nutricional por ID"""
    item = db.query(AvaliacaoNutricional).filter(AvaliacaoNutricional.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Avaliação Nutricional não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AvaliacaoNutricionalRead])
def listar_avaliacao_nutricional(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Nutritional Assessment / Listar Avaliação Nutricional"""
    return db.query(AvaliacaoNutricional).filter(
        AvaliacaoNutricional.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AvaliacaoNutricionalRead)
def atualizar_avaliacao_nutricional(
    item_id: int, 
    data: AvaliacaoNutricionalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Nutritional Assessment / Atualizar Avaliação Nutricional"""
    item = db.query(AvaliacaoNutricional).filter(AvaliacaoNutricional.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Avaliação Nutricional não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
