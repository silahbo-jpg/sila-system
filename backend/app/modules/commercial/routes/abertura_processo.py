from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.commercial.models.abertura_processo import AberturaProcesso
from app.modules.commercial.schemas.abertura_processo import AberturaProcessoCreate, AberturaProcessoRead, AberturaProcessoUpdate
from app.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/abertura-processo", tags=["Abertura Processo"])

@router.post("/", response_model=AberturaProcessoRead)
def criar_abertura_processo(
    data: AberturaProcessoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    db_item = AberturaProcesso(**data.dict(), municipe_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=AberturaProcessoRead)
def obter_abertura_processo(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    item = db.query(AberturaProcesso).filter(AberturaProcesso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Abertura Processo não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este recurso")
    return item

@router.get("/", response_model=list[AberturaProcessoRead])
def listar_abertura_processo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return db.query(AberturaProcesso).filter(AberturaProcesso.municipe_id == current_user.id).offset(skip).limit(limit).all()

@router.put("/id", response_model=AberturaProcessoRead)
def atualizar_abertura_processo(
    item_id: int,
    data: AberturaProcessoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    item = db.query(AberturaProcesso).filter(AberturaProcesso.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Abertura Processo não encontrado")
    if item.municipe_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este recurso")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

