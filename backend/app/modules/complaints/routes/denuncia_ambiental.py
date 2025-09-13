from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.denuncia_ambiental import DenunciaAmbiental
from app.modules.complaints.schemas.denuncia_ambiental import DenunciaAmbientalCreate, DenunciaAmbientalRead, DenunciaAmbientalUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/denuncia-ambiental", tags=["Denúncia Ambiental"])

@router.post("/", response_model=DenunciaAmbientalRead)
def criar_denuncia_ambiental(
    data: DenunciaAmbientalCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Environmental Report / Criar novo Denúncia Ambiental"""
    db_item = DenunciaAmbiental(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=DenunciaAmbientalRead)
def obter_denuncia_ambiental(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Environmental Report by ID / Obter Denúncia Ambiental por ID"""
    item = db.query(DenunciaAmbiental).filter(DenunciaAmbiental.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Denúncia Ambiental não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[DenunciaAmbientalRead])
def listar_denuncia_ambiental(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Environmental Report / Listar Denúncia Ambiental"""
    return db.query(DenunciaAmbiental).filter(
        DenunciaAmbiental.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=DenunciaAmbientalRead)
def atualizar_denuncia_ambiental(
    item_id: int, 
    data: DenunciaAmbientalUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Environmental Report / Atualizar Denúncia Ambiental"""
    item = db.query(DenunciaAmbiental).filter(DenunciaAmbiental.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Denúncia Ambiental não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
