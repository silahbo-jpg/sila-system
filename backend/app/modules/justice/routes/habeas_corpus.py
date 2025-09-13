from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.justice.models.habeas_corpus import HabeasCorpus
from app.modules.justice.schemas.habeas_corpus import HabeasCorpusCreate, HabeasCorpusRead, HabeasCorpusUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/habeas-corpus", tags=["Habeas Corpus"])

@router.post("/", response_model=HabeasCorpusRead)
def criar_habeas_corpus(
    data: HabeasCorpusCreate 
    current_user = Depends(get_current_active_user)
):
    """Create new Habeas Corpus / Criar novo Habeas Corpus"""
    db_item = HabeasCorpus(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=HabeasCorpusRead)
def obter_habeas_corpus(
    item_id: int 
    current_user = Depends(get_current_active_user)
):
    """Get Habeas Corpus by ID / Obter Habeas Corpus por ID"""
    item = db.query(HabeasCorpus).filter(HabeasCorpus.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Habeas Corpus não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=List[HabeasCorpusRead])
def listar_habeas_corpus(
    skip: int = 0, 
    limit: int = 100 
    current_user = Depends(get_current_active_user)
):
    """List Habeas Corpus / Listar Habeas Corpus"""
    return db.query(HabeasCorpus).filter(
        HabeasCorpus.municipe_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put("/id", response_model=HabeasCorpusRead)
def atualizar_habeas_corpus(
    item_id: int, 
    data: HabeasCorpusUpdate 
    current_user = Depends(get_current_active_user)
):
    """Update Habeas Corpus / Atualizar Habeas Corpus"""
    item = db.query(HabeasCorpus).filter(HabeasCorpus.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Habeas Corpus não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
