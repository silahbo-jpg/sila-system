from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.citizenship.models.regitro_eleitoral import RegitroEleitoral
from app.modules.citizenship.schemas.regitro_eleitoral import RegitroEleitoralCreate, RegitroEleitoralRead, RegitroEleitoralUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/regitro-eleitoral", tags=["Registro Eleitoral"])

@router.post("/", response_model=RegitroEleitoralRead)
def criar_regitro_eleitoral(
    data: RegitroEleitoralCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create new Electoral Registration / Criar novo Registro Eleitoral"""
    db_item = RegitroEleitoral(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=RegitroEleitoralRead)
def obter_regitro_eleitoral(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get Electoral Registration by ID / Obter Registro Eleitoral por ID"""
    item = db.query(RegitroEleitoral).filter(RegitroEleitoral.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registro Eleitoral não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[RegitroEleitoralRead])
def listar_regitro_eleitoral(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List Electoral Registration / Listar Registro Eleitoral"""
    return db.query(RegitroEleitoral).filter(
        RegitroEleitoral.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=RegitroEleitoralRead)
def atualizar_regitro_eleitoral(
    item_id: int, 
    data: RegitroEleitoralUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update Electoral Registration / Atualizar Registro Eleitoral"""
    item = db.query(RegitroEleitoral).filter(RegitroEleitoral.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Registro Eleitoral não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
