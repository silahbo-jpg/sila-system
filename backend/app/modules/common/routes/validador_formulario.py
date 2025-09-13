from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.common.models.validador_formulario import ValidadorFormulario
from app.modules.common.schemas.validador_formulario import ValidadorFormularioCreate, ValidadorFormularioRead, ValidadorFormularioUpdate

router = APIRouter(prefix="/internal/validador-formulario", tags=["Validador de Formulário"])

@router.post("/", response_model=ValidadorFormularioRead)
def criar_validador_formulario(data: ValidadorFormularioCreate):
    """Create new Form Validator / Criar novo Validador de Formulário"""
    db_item = ValidadorFormulario(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=ValidadorFormularioRead)
def obter_validador_formulario(item_id: int):
    """Get Form Validator by ID / Obter Validador de Formulário por ID"""
    item = db.query(ValidadorFormulario).filter(ValidadorFormulario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Validador de Formulário não encontrado")
    return item

@router.get("/", response_model=List[ValidadorFormularioRead])
def listar_validador_formulario(skip: int = 0, limit: int = 100):
    """List Form Validator / Listar Validador de Formulário"""
    return db.query(ValidadorFormulario).offset(skip).limit(limit).all()

@router.put("/id", response_model=ValidadorFormularioRead)
def atualizar_validador_formulario(item_id: int, data: ValidadorFormularioUpdate):
    """Update Form Validator / Atualizar Validador de Formulário"""
    item = db.query(ValidadorFormulario).filter(ValidadorFormulario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Validador de Formulário não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
