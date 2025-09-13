from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.registry.models.adocao_menor import AdocaoMenor
from app.modules.registry.schemas.adocao_menor import AdocaoMenorCreate, AdocaoMenorRead, AdocaoMenorUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/adocao-menor", tags=["Adoção de Menor"])

@router.post("/", response_model=AdocaoMenorRead)
def criar_adocao_menor(
    data: AdocaoMenorCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Child Adoption / Criar novo Adoção de Menor"""
    db_item = AdocaoMenor(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AdocaoMenorRead)
def obter_adocao_menor(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Child Adoption by ID / Obter Adoção de Menor por ID"""
    item = db.query(AdocaoMenor).filter(AdocaoMenor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Adoção de Menor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[AdocaoMenorRead])
def listar_adocao_menor(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Child Adoption / Listar Adoção de Menor"""
    return db.query(AdocaoMenor).filter(
        AdocaoMenor.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=AdocaoMenorRead)
def atualizar_adocao_menor(
    item_id: int, 
    data: AdocaoMenorUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Child Adoption / Atualizar Adoção de Menor"""
    item = db.query(AdocaoMenor).filter(AdocaoMenor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Adoção de Menor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
