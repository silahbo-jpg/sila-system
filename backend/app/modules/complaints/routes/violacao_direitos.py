from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.complaints.models.violacao_direitos import ViolacaoDireitos
from app.modules.complaints.schemas.violacao_direitos import ViolacaoDireitosCreate, ViolacaoDireitosRead, ViolacaoDireitosUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/violacao-direitos", tags=["Violação de Direitos"])

@router.post("/", response_model=ViolacaoDireitosRead)
def criar_violacao_direitos(
    data: ViolacaoDireitosCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Rights Violation / Criar novo Violação de Direitos"""
    db_item = ViolacaoDireitos(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ViolacaoDireitosRead)
def obter_violacao_direitos(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Rights Violation by ID / Obter Violação de Direitos por ID"""
    item = db.query(ViolacaoDireitos).filter(ViolacaoDireitos.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Violação de Direitos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[ViolacaoDireitosRead])
def listar_violacao_direitos(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Rights Violation / Listar Violação de Direitos"""
    return db.query(ViolacaoDireitos).filter(
        ViolacaoDireitos.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=ViolacaoDireitosRead)
def atualizar_violacao_direitos(
    item_id: int, 
    data: ViolacaoDireitosUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Rights Violation / Atualizar Violação de Direitos"""
    item = db.query(ViolacaoDireitos).filter(ViolacaoDireitos.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Violação de Direitos não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
