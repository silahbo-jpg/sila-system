from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.social.models.protecao_menor import ProtecaoMenor
from app.modules.social.schemas.protecao_menor import ProtecaoMenorCreate, ProtecaoMenorRead, ProtecaoMenorUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/protecao-menor", tags=["Proteção ao Menor"])

@router.post("/", response_model=ProtecaoMenorRead)
def criar_protecao_menor(
    data: ProtecaoMenorCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Child Protection / Criar novo Proteção ao Menor"""
    db_item = ProtecaoMenor(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ProtecaoMenorRead)
def obter_protecao_menor(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Child Protection by ID / Obter Proteção ao Menor por ID"""
    item = db.query(ProtecaoMenor).filter(ProtecaoMenor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Proteção ao Menor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ProtecaoMenorRead])
def listar_protecao_menor(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Child Protection / Listar Proteção ao Menor"""
    return db.query(ProtecaoMenor).filter(
        ProtecaoMenor.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ProtecaoMenorRead)
def atualizar_protecao_menor(
    item_id: int, 
    data: ProtecaoMenorUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Child Protection / Atualizar Proteção ao Menor"""
    item = db.query(ProtecaoMenor).filter(ProtecaoMenor.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Proteção ao Menor não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
